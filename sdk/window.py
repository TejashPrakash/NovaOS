from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, Any


class WindowState(Enum):
    """Possible window states."""
    NORMAL = "normal"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"
    FULLSCREEN = "fullscreen"
    HIDDEN = "hidden"


@dataclass
class WindowGeometry:
    """Window position and size."""
    x: int = 100
    y: int = 100
    width: int = 800
    height: int = 600
    
    def to_tuple(self) -> tuple[int, int, int, int]:
        """Convert to (x, y, width, height) tuple."""
        return (self.x, self.y, self.width, self.height)
    
    @classmethod
    def from_tuple(cls, geometry: tuple[int, int, int, int]) -> 'WindowGeometry':
        """Create from (x, y, width, height) tuple."""
        return cls(x=geometry[0], y=geometry[1], 
                  width=geometry[2], height=geometry[3])


class BaseWindow(ABC):
    """Base class for NovaOS application windows."""
    
    def __init__(self, title: str = "NovaOS Window"):
        self.title = title
        self.state = WindowState.NORMAL
        self.geometry = WindowGeometry()
        self._on_close_callback: Optional[Callable] = None
        self._on_focus_callback: Optional[Callable] = None
        self._on_resize_callback: Optional[Callable] = None
    
    @abstractmethod
    def show(self) -> None:
        """Show the window."""
        pass
    
    @abstractmethod
    def hide(self) -> None:
        """Hide the window."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the window."""
        pass
    
    @abstractmethod
    def focus(self) -> None:
        """Bring window to front and give focus."""
        pass
    
    def minimize(self) -> None:
        """Minimize the window."""
        self.state = WindowState.MINIMIZED
        self.hide()
    
    def maximize(self) -> None:
        """Maximize the window."""
        self.state = WindowState.MAXIMIZED
        self._apply_maximize()
    
    def restore(self) -> None:
        """Restore window to normal state."""
        self.state = WindowState.NORMAL
        self._apply_restore()
    
    def toggle_maximize(self) -> None:
        """Toggle between maximized and normal state."""
        if self.state == WindowState.MAXIMIZED:
            self.restore()
        else:
            self.maximize()
    
    def set_geometry(self, x: int, y: int, width: int, height: int) -> None:
        """Set window position and size."""
        self.geometry = WindowGeometry(x=x, y=y, width=width, height=height)
        self._apply_geometry()
    
    def set_title(self, title: str) -> None:
        """Set window title."""
        self.title = title
        self._apply_title()
    
    def on_close(self, callback: Callable) -> None:
        """Set callback for window close event."""
        self._on_close_callback = callback
    
    def on_focus(self, callback: Callable) -> None:
        """Set callback for window focus event."""
        self._on_focus_callback = callback
    
    def on_resize(self, callback: Callable) -> None:
        """Set callback for window resize event."""
        self._on_resize_callback = callback
    
    def _trigger_close(self) -> None:
        """Trigger the close callback if set."""
        if self._on_close_callback:
            self._on_close_callback()
    
    def _trigger_focus(self) -> None:
        """Trigger the focus callback if set."""
        if self._on_focus_callback:
            self._on_focus_callback()
    
    def _trigger_resize(self, width: int, height: int) -> None:
        """Trigger the resize callback if set."""
        if self._on_resize_callback:
            self._on_resize_callback(width, height)
    
    # Abstract methods for subclasses to implement
    @abstractmethod
    def _apply_maximize(self) -> None:
        """Apply maximize state to actual window."""
        pass
    
    @abstractmethod
    def _apply_restore(self) -> None:
        """Apply restore state to actual window."""
        pass
    
    @abstractmethod
    def _apply_geometry(self) -> None:
        """Apply geometry to actual window."""
        pass
    
    @abstractmethod
    def _apply_title(self) -> None:
        """Apply title to actual window."""
        pass


class WindowManager:
    """Manages multiple windows in NovaOS."""
    
    def __init__(self):
        self.windows: list[BaseWindow] = []
        self.active_window: Optional[BaseWindow] = None
        self.z_order: list[BaseWindow] = []
    
    def add_window(self, window: BaseWindow) -> None:
        """Add a window to management."""
        if window not in self.windows:
            self.windows.append(window)
            self.z_order.append(window)
            window.on_close(lambda: self.remove_window(window))
    
    def remove_window(self, window: BaseWindow) -> None:
        """Remove a window from management."""
        if window in self.windows:
            self.windows.remove(window)
        if window in self.z_order:
            self.z_order.remove(window)
        if self.active_window == window:
            self.active_window = None
    
    def set_active_window(self, window: BaseWindow) -> None:
        """Set the active/focused window."""
        if window in self.windows:
            self.active_window = window
            window.focus()
            self._bring_to_front(window)
    
    def get_active_window(self) -> Optional[BaseWindow]:
        """Get the currently active window."""
        return self.active_window
    
    def get_all_windows(self) -> list[BaseWindow]:
        """Get all managed windows."""
        return self.windows.copy()
    
    def _bring_to_front(self, window: BaseWindow) -> None:
        """Bring window to front of z-order."""
        if window in self.z_order:
            self.z_order.remove(window)
        self.z_order.append(window)
    
    def minimize_all(self) -> None:
        """Minimize all windows."""
        for window in self.windows:
            window.minimize()
    
    def close_all(self) -> None:
        """Close all windows."""
        for window in self.windows.copy():
            window.close()