from dataclasses import dataclass
from typing import Callable, Dict, Optional


@dataclass
class Shortcut:
    """Keyboard shortcut definition."""
    key: str
    description: str
    callback: Callable
    modifiers: str = ""  # e.g., "Ctrl+Alt+"


class ShortcutManager:
    """Keyboard shortcut manager for NovaOS."""
    
    def __init__(self, root):
        self.root = root
        self.shortcuts: Dict[str, Shortcut] = {}
        self._setup_default_shortcuts()
        
    def _setup_default_shortcuts(self):
        """Setup default NovaOS shortcuts."""
        self.register(
            Shortcut(
                key="space",
                modifiers="Control",
                description="Toggle Launcher",
                callback=self._toggle_launcher
            )
        )
        self.register(
            Shortcut(
                key="n",
                modifiers="Alt",
                description="Toggle AI Panel",
                callback=self._toggle_ai_panel
            )
        )
        self.register(
            Shortcut(
                key="Left",
                modifiers="Meta",
                description="Snap Left",
                callback=lambda: self._snap_window("left")
            )
        )
        self.register(
            Shortcut(
                key="Right",
                modifiers="Meta",
                description="Snap Right",
                callback=lambda: self._snap_window("right")
            )
        )
        
    def register(self, shortcut: Shortcut):
        """Register a keyboard shortcut."""
        key_sequence = f"{shortcut.modifiers}{shortcut.key}"
        self.shortcuts[key_sequence] = shortcut
        self._bind_shortcut(shortcut)
        
    def _bind_shortcut(self, shortcut: Shortcut):
        """Bind shortcut to callback."""
        if shortcut.modifiers:
            # Handle modifier keys
            event_pattern = f"<{shortcut.modifiers}-{shortcut.key}>"
        else:
            event_pattern = f"<{shortcut.key}>"
            
        self.root.bind_all(event_pattern, lambda e: shortcut.callback())
        
    def _toggle_launcher(self):
        """Toggle launcher (needs reference to launcher)."""
        # This would need to be connected to the actual launcher
        print("Toggle launcher")
        
    def _toggle_ai_panel(self):
        """Toggle AI panel (needs reference to AI panel)."""
        # This would need to be connected to the actual AI panel
        print("Toggle AI panel")
        
    def _snap_window(self, direction: str):
        """Snap focused window (needs reference to window manager)."""
        # This would need to be connected to the window manager
        print(f"Snap window {direction}")