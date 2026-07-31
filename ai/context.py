# TODO: Implement 
"""Conversation context helpers."""

from dataclasses import dataclass, field


@dataclass
class ConversationContext:
    """Stores conversation-specific state for the assistant."""

    user_id: str | None = None
    session_id: str | None = None
    metadata: dict = field(default_factory=dict)
