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


def test_novaos_attaches_desktop_icons_manager(monkeypatch):
    import core.app as app_module

    class FakeRoot:
        def title(self, *_args, **_kwargs):
            pass

        def geometry(self, *_args, **_kwargs):
            pass

        def minsize(self, *_args, **_kwargs):
            pass

        def bind_all(self, *_args, **_kwargs):
            pass

    class FakeKernel:
        def __init__(self):
            self.desktop = None
            self.dock = None
            self.window_manager = None

        def boot(self):
            pass

        def register_service(self, *_args, **_kwargs):
            pass

    class FakeDesktop:
        def __init__(self, root):
            self.root = root
            self.widget_layer = object()
            self.icon_layer = object()
            self.icons_manager = None

        def get_widget_layer(self):
            return self.widget_layer

        def get_icon_layer(self):
            return self.icon_layer

        def get_canvas(self):
            return object()

    class FakeDock:
        def __init__(self, root):
            self.root = root

        def set_launcher(self, *_args, **_kwargs):
            pass

        def add_start_button(self):
            pass

    class FakeWindowManager:
        def __init__(self, desktop, dock, kernel):
            self.desktop = desktop
            self.dock = dock
            self.kernel = kernel

    class FakeLauncher:
        def __init__(self, root, kernel):
            self.root = root
            self.kernel = kernel

        def hide(self):
            pass

    class FakeStartMenu:
        def __init__(self, widget_layer, window_manager):
            self.widget_layer = widget_layer
            self.window_manager = window_manager

    class FakeIconsManager:
        def __init__(self, desktop, window_manager):
            self.desktop = desktop
            self.window_manager = window_manager

    monkeypatch.setattr(app_module, 'ctk', type('FakeCtk', (), {
        'CTk': FakeRoot,
        'set_appearance_mode': staticmethod(lambda *_args, **_kwargs: None),
        'set_default_color_theme': staticmethod(lambda *_args, **_kwargs: None),
        'CTkButton': type('FakeButton', (), {'__init__': lambda self, *a, **k: None, 'place': lambda self, *a, **k: None}),
    }))
    monkeypatch.setattr(app_module, 'Kernel', FakeKernel)
    monkeypatch.setattr(app_module, 'Desktop', FakeDesktop)
    monkeypatch.setattr(app_module, 'Dock', FakeDock)
    monkeypatch.setattr(app_module, 'WindowManager', FakeWindowManager)
    monkeypatch.setattr(app_module, 'Launcher', FakeLauncher)
    monkeypatch.setattr(app_module, 'StartMenu', FakeStartMenu)
    monkeypatch.setattr(app_module, 'DesktopIconsManager', FakeIconsManager)

    nova = app_module.NovaOS()

    assert isinstance(nova.desktop.icons_manager, FakeIconsManager)
    assert nova.desktop.icons_manager.desktop is nova.desktop
    assert nova.desktop.icons_manager.window_manager is nova.window_manager