"""Short-term conversation memory for the assistant."""

from collections import deque


class MemoryStore:
    """Keeps the most recent conversation turns as (role, text) pairs."""

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._turns = deque(maxlen=max_turns)

    def remember(self, role: str, text: str) -> None:

        if role not in ("user", "assistant"):
            raise ValueError(f"Unknown role: {role}")

        self._turns.append((role, text))

    def turns(self) -> tuple[tuple[str, str], ...]:
        return tuple(self._turns)

    def clear(self) -> None:
        self._turns.clear()