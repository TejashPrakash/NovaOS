"""Kernel service that owns the NovaOS assistant."""

from ai.providers.voice import VoiceProvider

class AIService:
    """Initializes the assistant when a provider is available."""

    name = "ai"

    def __init__(self, kernel):
        self.kernel = kernel
        self.assistant = None  # Will be set when provider is available
        self.voice_provider = VoiceProvider()
        self.voice_enabled = False

        try:
            from ai.assistant import create_assistant

            self.assistant = create_assistant(kernel)
            if self.assistant:
                print("[AI Service] Nova AI assistant initialized")
        except Exception as e:
            print(f"[AI Service] Could not initialize assistant: {e}")

    def enable_voice(self):
        """Enable voice interaction."""
        if not self.voice_enabled:
            self.voice_enabled = True
            try:
                self.voice_provider.start_listening(self._handle_voice_input)
            except Exception as e:
                print(f"[AI Service] Failed to start voice provider: {e}")

    def disable_voice(self):
        """Disable voice interaction."""
        if self.voice_enabled:
            self.voice_enabled = False
            try:
                self.voice_provider.stop_listening()
            except Exception as e:
                print(f"[AI Service] Failed to stop voice provider: {e}")

    def _handle_voice_input(self, text: str):
        """Handle voice input."""
        if self.assistant is None:
            print("[AI Service] Assistant not available for voice input")
            return

        try:
            response = self.assistant.ask(text)
            # speak the response if TTS is available
            try:
                self.voice_provider.speak(response)
            except Exception:
                pass
        except Exception as e:
            print(f"[AI Service] Error handling voice input: {e}")

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