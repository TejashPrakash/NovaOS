"""Gemini backend built on the Interactions API."""

from google import genai

from core.config import CONFIG

from .base_provider import BaseProvider, ProviderError, Reply, ToolCall

class GeminiProvider(BaseProvider):

    name = "gemini"

    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or CONFIG.gemini_api_key
        self.model = model or CONFIG.gemini_model
        self._client = None

    # =====================================================

    @property
    def client(self):
        if self._client is None:
            if not self.api_key:
                raise ProviderError(
                    "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key."
                )
            self._client = genai.Client(api_key=self.api_key)

        return self._client

    # =====================================================

    def is_available(self):
        return bool(self.api_key)

    # =====================================================

    def complete(self, prompt, system=None, history=(), tools=()):
        request = {
            "model": self.model,
            "input": self._build_input(prompt, history),
            "store": False,
        }

        if system:
            request["system_instruction"] = system

        if tools:
            request["tools"] = [
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                }
                for tool in tools
            ]

        try:
            interaction = self.client.interactions.create(**request)
        except Exception as error:
            raise ProviderError(f"Gemini request failed: {error}") from error

        return self._parse(interaction)

    # =====================================================

    def _build_input(self, prompt, history):
        """Convert NovaOS history into stateless Interactions API input."""

        entries = []

        for role, text in history:
            entries.append(
                {
                    "type": "user_input" if role == "user" else "model_output",
                    "content": [{"type": "text", "text": text}],
                }
            )

        entries.append(
            {
                "type": "user_input",
                "content": [{"type": "text", "text": prompt}],
            }
        )

        return entries

    # =====================================================

    def _parse(self, interaction):
        """Pull tool calls and text out of the returned interaction steps."""

        calls = []

        for step in interaction.steps:
            if getattr(step, "type", None) != "function_call":
                continue

            arguments = getattr(step, "arguments", None) or {}

            calls.append(
                ToolCall(
                    name=step.name,
                    arguments=dict(arguments),
                )
            )

        return Reply(
            text=interaction.output_text or "",
            tool_calls=tuple(calls),
        )