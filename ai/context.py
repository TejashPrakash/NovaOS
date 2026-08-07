"""Conversation context passed through the AI layer."""

from dataclasses import dataclass, field

from ai.memory import MemoryStore


@dataclass
class ConversationContext:
    """Per-conversation state: who is talking and what was said before."""

    user_id: str | None = None
    session_id: str | None = None
    metadata: dict = field(default_factory=dict)
    memory: MemoryStore = field(default_factory=MemoryStore)

    @property
    def history(self) -> tuple[tuple[str, str], ...]:
        return self.memory.turns()

    def remember(self, role: str, text: str) -> None:
        self.memory.remember(role, text)