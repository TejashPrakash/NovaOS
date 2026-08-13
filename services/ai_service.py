"""Kernel service that owns the NovaOS assistant."""


class AIService:
    """Initializes the assistant when a provider is available."""

    name = "ai"

    def __init__(self, kernel):
        self.kernel = kernel
        self.assistant = None  # Will be set when provider is available

        try:
            from ai.assistant import create_assistant

            self.assistant = create_assistant(kernel)
            if self.assistant:
                print("[AI Service] Nova AI assistant initialized")
        except Exception as e:
            print(f"[AI Service] Could not initialize assistant: {e}")

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