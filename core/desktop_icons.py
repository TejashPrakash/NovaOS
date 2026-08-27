import customtkinter as ctk


class DesktopIcon(ctk.CTkFrame):
    """Vibrant desktop icon with glow effects."""
    
    def __init__(self, parent, icon_text, app_name, callback, **kwargs):
        super().__init__(
            parent,
            width=90,
            height=100,
            fg_color="transparent",
            **kwargs
        )
        self.callback = callback
        self.app_name = app_name
        self._setup_icon(icon_text, app_name)
        
    def _setup_icon(self, icon_text, app_name):
        """Setup vibrant icon with glow background."""
        # Glow background frame
        self.glow_frame = ctk.CTkFrame(
            self,
            width=70, height=70,
            fg_color="#0D1A25",
            corner_radius=16,
            border_width=1,
            border_color="#0A1520"
        )
        self.glow_frame.pack(pady=(8, 2))
        self.glow_frame.pack_propagate(False)

        self.icon_label = ctk.CTkLabel(
            self.glow_frame,
            text=icon_text,
            font=("Segoe UI Emoji", 30),
            text_color="#FFFFFF"
        )
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.name_label = ctk.CTkLabel(
            self,
            text=app_name,
            font=("Segoe UI", 10, "bold"),
            text_color="#BBBBBB"
        )
        self.name_label.pack()
        
        # Hover effects
        for widget in (self, self.glow_frame, self.icon_label, self.name_label):
            widget.bind("<Button-1>", lambda e: self.callback())
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, e=None):
        """Glow on hover."""
        self.glow_frame.configure(
            fg_color="#0D2833",
            border_color="#00E5FF"
        )
        self.name_label.configure(text_color="#00E5FF")

    def _on_leave(self, e=None):
        """Remove glow."""
        self.glow_frame.configure(
            fg_color="#0D1A25",
            border_color="#0A1520"
        )
        self.name_label.configure(text_color="#BBBBBB")


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
            ("🌤", "Weather"),
            ("📅", "Calendar"),
            ("📊", "System Monitor"),
            ("🎵", "Music Player"),
            ("👁", "Viewer"),
            ("⚙️", "Settings"),
        ]
        
        for i, (icon, app_name) in enumerate(default_apps):
            icon_widget = DesktopIcon(
                self.desktop.get_icon_layer(),
                icon,
                app_name,
                lambda a=app_name: self._launch_app(a)
            )
            
            # Position in grid (top-left, 3 columns, below Smart Hub pill at y=20)
            row = i // 3
            col = i % 3
            icon_widget.place(x=30 + col * 110, y=80 + row * 120)
            self.icons.append(icon_widget)
            
    def _launch_app(self, app_name):
        """Launch application from desktop icon."""
        self.window_manager.kernel.process_manager.start_process(app_name)