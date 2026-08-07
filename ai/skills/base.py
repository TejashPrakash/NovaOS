from collections.abc import Callable
from dataclasses import dataclass

from ai.providers import Tool


class SkillError(RuntimeError):
    """Raised when a skill is given arguments it cannot act on."""


@dataclass(frozen=True)
class Skill:
    """One capability NovaOS exposes to the model."""

    tool: Tool
    run: Callable[..., str]

    @property
    def name(self) -> str:
        return self.tool.name


def string_parameters(**fields: str) -> dict:
    """Build a JSON schema where every field is a required string."""

    return {
        "type": "object",
        "properties": {
            name: {"type": "string", "description": description}
            for name, description in fields.items()
        },
        "required": list(fields),
    }