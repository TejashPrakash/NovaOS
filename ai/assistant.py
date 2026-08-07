"""Entry point for the NovaOS assistant."""

from ai.context import ConversationContext
from ai.providers import ProviderError, get_provider
from ai.router import Router


class Assistant:
    """One conversation with Nova, bound to a kernel it can drive."""

    def __init__(self, kernel=None, provider=None, router=None):
        self.kernel = kernel
        self.context = ConversationContext()
        self.router = router or Router(provider or get_provider(), kernel)

    # =====================================================

    @property
    def provider_name(self):
        return self.router.provider.name

    # =====================================================

    def ask(self, message: str) -> str:
        """Answer a user message, running any skills the model chooses."""

        message = message.strip()

        if not message:
            return "Ask me something."

        reply = self.router.route(message, self.context)

        self.context.remember("user", message)
        self.context.remember("assistant", reply)

        return reply

    # =====================================================

    def reset(self) -> None:
        self.context.memory.clear()


def create_assistant(kernel=None):
    """Build an assistant, or return None when no provider is configured."""

    try:
        return Assistant(kernel)
    except ProviderError as error:
        print(f"[AI] disabled: {error}")
        return None