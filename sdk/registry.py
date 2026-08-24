from typing import Any, Dict, Type, Optional


class Registry:
    """Generic registry for NovaOS components."""
    
    def __init__(self):
        self._items: Dict[str, Any] = {}
        self._lock = False
    
    def register(self, name: str, item: Any) -> None:
        """Register an item with the given name."""
        if self._lock:
            raise RuntimeError("Registry is locked and cannot be modified")
        if name in self._items:
            raise ValueError(f"Item '{name}' is already registered")
        self._items[name] = item
    
    def unregister(self, name: str) -> None:
        """Unregister an item by name."""
        if self._lock:
            raise RuntimeError("Registry is locked and cannot be modified")
        if name not in self._items:
            raise KeyError(f"Item '{name}' is not registered")
        del self._items[name]
    
    def get(self, name: str, default: Any = None) -> Any:
        """Get an item by name, returning default if not found."""
        return self._items.get(name, default)
    
    def get_or_raise(self, name: str) -> Any:
        """Get an item by name, raising KeyError if not found."""
        if name not in self._items:
            raise KeyError(f"Item '{name}' is not registered")
        return self._items[name]
    
    def list(self) -> list[str]:
        """List all registered item names."""
        return list(self._items.keys())
    
    def items(self) -> Dict[str, Any]:
        """Get all registered items as a dictionary."""
        return self._items.copy()
    
    def contains(self, name: str) -> bool:
        """Check if an item is registered."""
        return name in self._items
    
    def clear(self) -> None:
        """Clear all registered items."""
        if self._lock:
            raise RuntimeError("Registry is locked and cannot be modified")
        self._items.clear()
    
    def lock(self) -> None:
        """Lock the registry to prevent further modifications."""
        self._lock = True
    
    def unlock(self) -> None:
        """Unlock the registry to allow modifications."""
        self._lock = False


class TypedRegistry(Registry):
    """Type-safe registry for specific component types."""
    
    def __init__(self, item_type: Type):
        super().__init__()
        self._item_type = item_type
    
    def register(self, name: str, item: Any) -> None:
        """Register an item with type checking."""
        if not isinstance(item, self._item_type):
            raise TypeError(
                f"Expected {self._item_type.__name__}, got {type(item).__name__}"
            )
        super().register(name, item)


# Global registries for common NovaOS components
APP_REGISTRY = TypedRegistry(object)  # Will be populated with app classes
SERVICE_REGISTRY = Registry()
COMMAND_REGISTRY = Registry()
PLUGIN_REGISTRY = Registry()