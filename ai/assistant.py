# TODO: Implement 
"""Main assistant entry point."""

from .context import ConversationContext
from .memory import MemoryStore
from .router import Router


class Assistant:
    """A lightweight AI assistant shell for NovaOS."""

    def __init__(self, router: Router | None = None, memory: MemoryStore | None = None):
        self.router = router or Router()
        self.memory = memory or MemoryStore()

    def handle_message(self, message: str, context: ConversationContext | None = None) -> str:
        """Route a message to the appropriate skill or provider."""
        if context is None:
            context = ConversationContext()
        self.memory.append(message)
        return self.router.route(message, context)
