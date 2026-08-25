import customtkinter as ctk
from typing import List, Callable, Optional


class ContextMenu(ctk.CTkFrame):
    """Context menu for right-click actions."""
    
    def __init__(self, parent, x, y, items: List[dict], **kwargs):
        super().__init__(
            parent,
            fg_color="#252B3B",
            corner_radius=8,
            border_width=1,
            border_color="#2F3545",
            **kwargs
        )
        self.items = items
        self._setup_menu()
        self.place(x=x, y=y)
        
        # Close when clicking outside
        parent.bind("<Button-1>", self._close_on_click, add="+")
        
    def _setup_menu(self):
        """Setup menu items."""
        for item in self.items:
            if item.get("separator"):
                separator = ctk.CTkFrame(
                    self,
                    height=1,
                    fg_color="#2F3545"
                )
                separator.pack(fill="x", padx=5, pady=2)
            else:
                menu_item = ctk.CTkButton(
                    self,
                    text=item["text"],
                    fg_color="transparent",
                    text_color="#BBBBBB",
                    hover_color="#00E5FF",
                    hover_text_color="black",
                    corner_radius=4,
                    command=item["callback"]
                )
                menu_item.pack(fill="x", padx=5, pady=2)
                
    def _close_on_click(self, event):
        """Close menu when clicking outside."""
        self.destroy()
        
    def destroy(self):
        """Clean up menu."""
        try:
            self.master.unbind("<Button-1>", self._close_on_click)
        except Exception:
            pass
        super().destroy()


class ContextMenuManager:
    """Manage context menus across the desktop."""
    
    def __init__(self, desktop):
        self.desktop = desktop
        self.current_menu = None
        self._setup_desktop_menu()
        
    def _setup_desktop_menu(self):
        """Setup desktop context menu."""
        self.desktop.get_canvas().bind("<Button-3>", self._show_desktop_menu)
        
    def _show_desktop_menu(self, event):
        """Show desktop context menu."""
        items = [
            {"text": "🔄 Refresh", "callback": self._refresh_desktop},
            {"separator": True},
            {"text": "⚙️ Settings", "callback": self._open_settings},
            {"text": "🎨 Change Background", "callback": self._change_background},
            {"separator": True},
            {"text": "📝 New Note", "callback": self._new_note},
            {"text": "🧮 Calculator", "callback": self._open_calculator}
        ]
        
        if self.current_menu:
            self.current_menu.destroy()
            
        self.current_menu = ContextMenu(
            self.desktop.get_widget_layer(),
            event.x,
            event.y,
            items
        )
        
    def _refresh_desktop(self):
        """Refresh desktop."""
        print("Refresh desktop")
        
    def _open_settings(self):
        """Open settings."""
        if hasattr(self.desktop, 'window_manager'):
            self.desktop.window_manager.kernel.process_manager.start_process("Settings")
            
    def _change_background(self):
        """Change background."""
        print("Change background")
        
    def _new_note(self):
        """Create new note."""
        if hasattr(self.desktop, 'window_manager'):
            self.desktop.window_manager.kernel.process_manager.start_process("Notes")
            
    def _open_calculator(self):
        """Open calculator."""
        if hasattr(self.desktop, 'window_manager'):
            self.desktop.window_manager.kernel.process_manager.start_process("Calculator")