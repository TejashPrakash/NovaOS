# TODO: Implement 
"""Gemini provider stub."""

from .base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    def generate(self, prompt: str) -> str:
        return f"[gemini] {prompt}"
