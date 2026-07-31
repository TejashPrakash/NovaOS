# TODO: Implement 
"""Simple memory store for assistant history."""

from collections import deque


class MemoryStore:
    """Stores recent assistant-related messages."""

    def __init__(self, max_items: int = 50):
        self.max_items = max_items
        self._history = deque(maxlen=max_items)

    def append(self, item: str) -> None:
        self._history.append(item)

    def get_history(self) -> list[str]:
        return list(self._history)
