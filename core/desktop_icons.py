import customtkinter as ctk


class DesktopIcon(ctk.CTkFrame):
    """Single desktop icon."""
    
    def __init__(self, parent, icon_text, app_name, callback, **kwargs):
        super().__init__(
            parent,
            width=80,
            height=90,
            fg_color="transparent",
            **kwargs
        )
        self.callback = callback
        self._setup_icon(icon_text, app_name)
        
    def _setup_icon(self, icon_text, app_name):
        """Setup icon appearance."""
        self.icon_label = ctk.CTkLabel(
            self,
            text=icon_text,
            font=("Segoe UI", 32)
        )
        self.icon_label.pack(pady=(10, 5))
        
        self.name_label = ctk.CTkLabel(
            self,
            text=app_name,
            font=("Segoe UI", 10),
            text_color="#BBBBBB"
        )
        self.name_label.pack()
        
        self.bind("<Button-1>", lambda e: self.callback())
        self.icon_label.bind("<Button-1>", lambda e: self.callback())
        self.name_label.bind("<Button-1>", lambda e: self.callback())


class DesktopIconsManager:
    """Manage desktop icons."""
    
    def __init__(self, desktop, window_manager):
        self.desktop = desktop
        self.window_manager = window_manager
        self.icons = []
        self._setup_default_icons()
        
    def _setup_default_icons(self):
        """Setup default desktop icons."""
        default_apps = [
            ("🌐", "Browser"),
            ("📝", "Notes"),
            ("🧮", "Calculator"),
            ("📁", "Files"),
            (">_", "Terminal"),
            ("📝", "Editor"),
            ("⚙️", "Settings"),
        ]
        
        for i, (icon, app_name) in enumerate(default_apps):
            icon_widget = DesktopIcon(
                self.desktop.get_icon_layer(),
                icon,
                app_name,
                lambda a=app_name: self._launch_app(a)
            )
            
            # Position in grid
            row = i // 5
            col = i % 5
            icon_widget.place(x=30 + col * 100, y=30 + row * 110)
            self.icons.append(icon_widget)
            
    def _launch_app(self, app_name):
        """Launch application from desktop icon."""
        self.window_manager.kernel.process_manager.start_process(app_name)