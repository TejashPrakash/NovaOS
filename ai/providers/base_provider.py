# TODO: Implement 
"""Base interface for AI providers."""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Common base class for AI providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        raise NotImplementedError
