import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Runtime configuration for NovaOS, sourced from the environment."""

    provider: str
    gemini_api_key: str
    gemini_model: str
    ollama_host: str
    ollama_model: str

    @classmethod
    def load(cls):
        return cls(
            provider=os.getenv("NOVA_PROVIDER", "gemini"),
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            gemini_model=os.getenv("NOVA_GEMINI_MODEL", "gemini-3.6-flash"),
            ollama_host=os.getenv("NOVA_OLLAMA_HOST", "http://localhost:11434"),
            ollama_model=os.getenv("NOVA_OLLAMA_MODEL", "llama3.1"),
        )


CONFIG = Config.load()