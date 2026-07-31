# TODO: Implement 
"""OpenAI provider stub."""

from .base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    def generate(self, prompt: str) -> str:
        return f"[openai] {prompt}"
