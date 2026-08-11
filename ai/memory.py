"""Short-term conversation memory for the assistant with persistence."""

import json
import os
from collections import deque
from datetime import datetime
from typing import Optional


class MemoryStore:
    """Keeps the most recent conversation turns as (role, text) pairs with file persistence."""

    def __init__(self, max_turns: int = 20, persist_file: Optional[str] = None):
        self.max_turns = max_turns
        self._turns = deque(maxlen=max_turns)
        self.persist_file = persist_file
        self._load_from_disk()

    def remember(self, role: str, text: str) -> None:

        if role not in ("user", "assistant"):
            raise ValueError(f"Unknown role: {role}")

        self._turns.append((role, text, datetime.now().isoformat()))
        self._save_to_disk()

    def turns(self) -> tuple[tuple[str, str], ...]:
        """Return turns without timestamps for AI processing."""
        return tuple((role, text) for role, text, _ in self._turns)

    def turns_with_metadata(self) -> tuple[tuple[str, str, str], ...]:
        """Return turns with timestamps for analysis."""
        return tuple(self._turns)

    def clear(self) -> None:
        self._turns.clear()
        self._save_to_disk()

    def _load_from_disk(self):
        """Load conversation history from disk if persistence is enabled."""
        if not self.persist_file or not os.path.exists(self.persist_file):
            return

        try:
            with open(self.persist_file, 'r') as f:
                data = json.load(f)
                self._turns = deque(
                    (turn['role'], turn['text'], turn['timestamp']) 
                    for turn in data.get('turns', [])
                )
        except Exception as e:
            print(f"[Memory] Failed to load from disk: {e}")

    def _save_to_disk(self):
        """Save conversation history to disk if persistence is enabled."""
        if not self.persist_file:
            return

        try:
            os.makedirs(os.path.dirname(self.persist_file), exist_ok=True)
            with open(self.persist_file, 'w') as f:
                json.dump({
                    'turns': [
                        {'role': role, 'text': text, 'timestamp': timestamp}
                        for role, text, timestamp in self._turns
                    ],
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"[Memory] Failed to save to disk: {e}")

    def search_history(self, query: str) -> list:
        """Search conversation history for specific terms."""
        query_lower = query.lower()
        results = []
        for role, text, timestamp in self._turns:
            if query_lower in text.lower():
                results.append({
                    'role': role,
                    'text': text,
                    'timestamp': timestamp
                })
        return results