from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Command(ABC):
    """Base class for NovaOS commands."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the command name."""
        pass
    
    @abstractmethod
    def execute(self, kernel, *args, **kwargs) -> Any:
        """Execute the command."""
        pass
    
    @property
    def description(self) -> str:
        """Return command description."""
        return f"Command: {self.name}"


class CommandRegistry:
    """Registry for managing NovaOS commands."""
    
    def __init__(self):
        self._commands: Dict[str, Command] = {}
    
    def register(self, command: Command) -> None:
        """Register a command."""
        name = command.name
        if name in self._commands:
            raise ValueError(f"Command '{name}' already registered")
        self._commands[name] = command
    
    def unregister(self, name: str) -> None:
        """Unregister a command."""
        if name not in self._commands:
            raise KeyError(f"Command '{name}' not registered")
        del self._commands[name]
    
    def execute(self, kernel, name: str, *args, **kwargs) -> Any:
        """Execute a command by name."""
        command = self._commands.get(name)
        if not command:
            raise KeyError(f"Unknown command: {name}")
        return command.execute(kernel, *args, **kwargs)
    
    def get(self, name: str) -> Optional[Command]:
        """Get a command by name."""
        return self._commands.get(name)
    
    def all(self) -> list[str]:
        """Get all registered command names."""
        return list(self._commands.keys())
    
    def list_commands(self) -> Dict[str, str]:
        """List all commands with descriptions."""
        return {name: cmd.description for name, cmd in self._commands.items()}