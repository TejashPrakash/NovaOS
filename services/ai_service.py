"""Kernel service that owns the NovaOS assistant."""

from ai.assistant import create_assistant


class AIService:
    """Lazily builds the assistant so NovaOS still boots without a provider."""

    name = "ai"

    def __init__(self, kernel):
        self.kernel = kernel
        self._assistant = None
        self._tried = False

    # =====================================================

    @property
    def assistant(self):

        if not self._tried:
            self._assistant = create_assistant(self.kernel)
            self._tried = True

        return self._assistant

    # =====================================================

    def is_available(self):
        return self.assistant is not None

    # =====================================================

    def ask(self, message):
        """Answer a user message, or explain why the AI layer is off."""

        if self.assistant is None:
            return (
                "Nova AI is not configured. Set GEMINI_API_KEY in .env "
                "or start Ollama, then restart NovaOS."
            )

        reply = self.assistant.ask(message)

        self.kernel.events.emit("ai_reply", message, reply)

        return reply