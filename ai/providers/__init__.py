"""Provider selection for the NovaOS AI layer."""

from core.config import CONFIG

from .base_provider import BaseProvider, ProviderError, Reply, Tool, ToolCall
from .gemini import GeminiProvider
from .ollama import OllamaProvider

PROVIDERS = {
    "gemini": GeminiProvider,
    "ollama": OllamaProvider,
}

__all__ = [
    "BaseProvider",
    "ProviderError",
    "Reply",
    "Tool",
    "ToolCall",
    "get_provider",
]


def get_provider(name=None):
    """Return the configured provider, falling back to a reachable one."""

    name = name or CONFIG.provider

    if name not in PROVIDERS:
        raise ProviderError(f"Unknown provider: {name}")

    provider = PROVIDERS[name]()

    if provider.is_available():
        return provider

    for fallback_name, fallback_class in PROVIDERS.items():

        if fallback_name == name:
            continue

        fallback = fallback_class()

        if fallback.is_available():
            print(f"[AI] {name} unavailable, falling back to {fallback_name}")
            return fallback

    raise ProviderError(
        "No AI provider is available. Set GEMINI_API_KEY in .env or start Ollama."
    )