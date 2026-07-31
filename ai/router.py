# TODO: Implement 
"""Routing logic for assistant requests."""

from .context import ConversationContext


class Router:
    """Routes incoming prompts to the right skill or provider."""

    def route(self, message: str, context: ConversationContext) -> str:
        """Return a simple placeholder response for now."""
        return f"[router] Received: {message}"
