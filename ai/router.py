"""Turns a user instruction into provider calls and executed skills."""

from ai import skills
from ai.context import ConversationContext
from ai.providers import ProviderError
from ai.skills import SkillError

SYSTEM_PROMPT = (
    "You are Nova, the assistant built into the NovaOS desktop operating system. "
    "You control the desktop through the tools you are given: open and close apps, "
    "list apps, read and write notes, and report system status. "
    "Call a tool whenever the user asks for something the OS can do, instead of "
    "describing how to do it. Keep replies to one or two short sentences."
)


class Router:
    """Sends a prompt to the provider and runs whatever skills it asks for."""

    def __init__(self, provider, kernel=None, tools=None):
        self.provider = provider
        self.kernel = kernel
        self.tools = skills.TOOLS if tools is None else tools

    # =====================================================

    def route(self, message: str, context: ConversationContext | None = None) -> str:

        history = () if context is None else tuple(context.history)

        try:
            reply = self.provider.complete(
                message,
                system=SYSTEM_PROMPT,
                history=history,
                tools=self.tools,
            )
        except ProviderError as error:
            return f"Nova is unavailable: {error}"

        if not reply.is_tool_call:
            return reply.text or "I did not understand that."

        results = [self._run(call) for call in reply.tool_calls]

        return " ".join(part for part in [reply.text, *results] if part)

    # =====================================================

    def _run(self, call) -> str:
        """Execute one tool call, reporting failures as text the user can act on."""

        skill = skills.find(call.name)

        if skill is None:
            return f"I tried to use an unknown skill: {call.name}."

        try:
            return skill.run(self.kernel, **call.arguments)
        except SkillError as error:
            return f"I could not do that: {error}"
        except Exception as error:
            print(f"[AI] skill {call.name} failed: {error!r}")
            return f"{call.name} failed unexpectedly."