# TODO: Implement 
"""Ollama provider stub."""

from .base_provider import BaseProvider


class OllamaProvider(BaseProvider):
    def generate(self, prompt: str) -> str:
        return f"[ollama] {prompt}"
