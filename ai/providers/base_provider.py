"""Provider-neutral interface for NovaOS AI backends."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ToolCall:
    """A skill the model wants NovaOS to run."""

    name: str
    arguments: dict


@dataclass(frozen=True)
class Reply:
    """A provider response: free text, tool calls, or both."""

    text: str = ""
    tool_calls: tuple[ToolCall, ...] = ()

    @property
    def is_tool_call(self):
        return bool(self.tool_calls)


@dataclass(frozen=True)
class Tool:
    """A skill description the model can choose from."""

    name: str
    description: str
    parameters: dict = field(default_factory=lambda: {"type": "object", "properties": {}})


class ProviderError(RuntimeError):
    """Raised when a backend is misconfigured or unreachable."""


class BaseProvider(ABC):
    """Every AI backend NovaOS supports implements this."""

    name = "base"

    @abstractmethod
    def is_available(self):
        """Return True when this backend is configured and reachable."""

    @abstractmethod
    def complete(self, prompt, system=None, history=(), tools=()):
        """Return a Reply for prompt.

        history is a sequence of (role, text) pairs where role is
        "user" or "assistant". tools is a sequence of Tool objects.
        """