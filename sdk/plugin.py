from abc import ABC, abstractmethod
from typing import Optional, Dict

class Plugin(ABC):
    """Base class for NovaOS plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the plugin name."""
        pass
    
    @property
    def version(self) -> str:
        """Return the plugin version."""
        return "1.0.0"
    
    @property
    def description(self) -> str:
        """Return the plugin description."""
        return f"Plugin: {self.name}"
    
    def on_load(self, kernel) -> None:
        """Called when the plugin is loaded."""
        print(f"[Plugin] Loading {self.name} v{self.version}")
    
    def on_unload(self, kernel) -> None:
        """Called when the plugin is unloaded."""
        print(f"[Plugin] Unloading {self.name}")
    
    def on_enable(self, kernel) -> None:
        """Called when the plugin is enabled."""
        pass
    
    def on_disable(self, kernel) -> None:
        """Called when the plugin is disabled."""
        pass


class PluginManager:
    """Manager for NovaOS plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._enabled: set[str] = set()
    
    def load(self, plugin: Plugin, kernel) -> None:
        """Load a plugin."""
        name = plugin.name
        if name in self._plugins:
            raise ValueError(f"Plugin '{name}' already loaded")
        
        plugin.on_load(kernel)
        self._plugins[name] = plugin
        self._enabled.add(name)
    
    def unload(self, name: str, kernel) -> None:
        """Unload a plugin."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not loaded")
        
        plugin = self._plugins[name]
        plugin.on_unload(kernel)
        del self._plugins[name]
        self._enabled.discard(name)
    
    def enable(self, name: str, kernel) -> None:
        """Enable a plugin."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not loaded")
        
        if name in self._enabled:
            return
        
        plugin = self._plugins[name]
        plugin.on_enable(kernel)
        self._enabled.add(name)
    
    def disable(self, name: str, kernel) -> None:
        """Disable a plugin."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not loaded")
        
        if name not in self._enabled:
            return
        
        plugin = self._plugins[name]
        plugin.on_disable(kernel)
        self._enabled.discard(name)
    
    def get(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self._plugins.get(name)
    
    def list(self) -> list[str]:
        """List all loaded plugins."""
        return list(self._plugins.keys())
    
    def list_enabled(self) -> list[str]:
        """List enabled plugins."""
        return list(self._enabled)