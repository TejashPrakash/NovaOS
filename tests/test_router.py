"""Router tests: no API key, no network, no GUI."""

from ai.context import ConversationContext
from ai.providers import BaseProvider, ProviderError, Reply, ToolCall
from ai.router import Router


class FakeKernel:
    """Records the commands a skill asks the kernel to run."""

    def __init__(self, results=None):
        self.calls = []
        self.results = results or {}
        self.commands = self

    def execute(self, kernel, name, *args):
        self.calls.append((name, args))
        return self.results.get(name, True)


class FakeProvider(BaseProvider):
    """Returns a scripted Reply and remembers what it was asked."""

    name = "fake"

    def __init__(self, reply=None, error=None):
        self.reply = reply or Reply(text="hello")
        self.error = error
        self.requests = []

    def is_available(self):
        return True

    def complete(self, prompt, system=None, history=(), tools=()):
        self.requests.append((prompt, system, tuple(history), tuple(tools)))

        if self.error:
            raise self.error

        return self.reply


def test_plain_text_reply_is_returned_unchanged():
    router = Router(FakeProvider(Reply(text="Good morning.")), FakeKernel())

    assert router.route("hi") == "Good morning."


def test_tool_call_runs_the_skill_against_the_kernel():
    kernel = FakeKernel()
    provider = FakeProvider(
        Reply(tool_calls=(ToolCall(name="open_app", arguments={"app_name": "Notes"}),))
    )

    assert Router(provider, kernel).route("open notes") == "Opened Notes."
    assert kernel.calls == [("open_app", ("Notes",))]


def test_unknown_app_is_reported_not_raised():
    kernel = FakeKernel(results={"open_app": False})
    provider = FakeProvider(
        Reply(tool_calls=(ToolCall(name="open_app", arguments={"app_name": "Excel"}),))
    )

    assert "could not do that" in Router(provider, kernel).route("open excel")


def test_unknown_skill_is_reported():
    provider = FakeProvider(
        Reply(tool_calls=(ToolCall(name="mine_bitcoin", arguments={}),))
    )

    assert "unknown skill" in Router(provider, FakeKernel()).route("get rich")


def test_provider_failure_becomes_a_readable_message():
    provider = FakeProvider(error=ProviderError("no key"))

    assert Router(provider, FakeKernel()).route("hi") == "Nova is unavailable: no key"


def test_history_and_tools_are_forwarded_to_the_provider():
    provider = FakeProvider()
    context = ConversationContext()
    context.remember("user", "open notes")
    context.remember("assistant", "Opened Notes.")

    Router(provider, FakeKernel()).route("close it", context)

    prompt, system, history, tools = provider.requests[0]

    assert prompt == "close it"
    assert "NovaOS" in system
    assert history == (("user", "open notes"), ("assistant", "Opened Notes."))
    assert "open_app" in {tool.name for tool in tools}


def test_multiple_tool_calls_are_all_executed():
    kernel = FakeKernel()
    provider = FakeProvider(
        Reply(
            text="On it.",
            tool_calls=(
                ToolCall(name="open_app", arguments={"app_name": "Notes"}),
                ToolCall(name="open_app", arguments={"app_name": "Browser"}),
            ),
        )
    )

    reply = Router(provider, kernel).route("open notes and browser")

    assert reply == "On it. Opened Notes. Opened Browser."
    assert kernel.calls == [("open_app", ("Notes",)), ("open_app", ("Browser",))]