import customtkinter as ctk
from apps.registry import APP_REGISTRY
from widgets.glass import GlassFrame
from core.theme import ThemeManager


class StartMenu(GlassFrame):
    """NovaOS Start Menu with premium glassmorphism design."""
    
    def __init__(self, master, window_manager, **kwargs):
        self.theme = ThemeManager()
        
        super().__init__(
            master,
            width=500,
            height=450,
            blur_amount=20,
            opacity=0.9,
            fg_color=self.theme.get_color("surface"),
            corner_radius=20,
            border_width=2,
            border_color=self.theme.get_color("primary"),
            **kwargs
        )
        
        self.window_manager = window_manager
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup start menu UI with theme colors."""
        # Premium search bar
        self.search = ctk.CTkEntry(
            self,
            placeholder_text="Search apps...",
            height=40,
            fg_color=self.theme.get_color("surface_light"),
            text_color=self.theme.get_color("text_primary"),
            placeholder_text_color=self.theme.get_color("text_muted"),
            corner_radius=10,
            border_width=1,
            border_color=self.theme.get_color("primary")
        )
        self.search.pack(fill="x", padx=20, pady=15)
        self.search.bind("<KeyRelease>", self._filter_apps)
        
        # Apps grid
        self.apps_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.apps_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self._build_app_grid()
        
        # Bottom section
        self._setup_bottom_section()
    
    def _build_app_grid(self):
        """Build application grid with theme colors."""
        for widget in self.apps_frame.winfo_children():
            widget.destroy()
        
        apps = [
            ("🌐", "Browser"),
            ("📝", "Notes"),
            ("🧮", "Calculator"),
            ("📁", "Files"),
            (">_", "Terminal"),
            ("🌤", "Weather"),
            ("📅", "Calendar"),
            ("📊", "System Monitor"),
            ("⚙️", "Settings"),
            ("🎵", "Music Player")
        ]
        
        for i, (icon, app_name) in enumerate(apps):
            app_button = ctk.CTkButton(
                self.apps_frame,
                text=f"{icon}\n{app_name}",
                width=100,
                height=80,
                fg_color=self.theme.get_color("surface_light"),
                text_color=self.theme.get_color("primary"),
                hover_color=self.theme.get_color("primary"),
                corner_radius=12,
                border_width=1,
                border_color=self.theme.get_color("primary"),
                command=lambda a=app_name: self._launch_app(a)
            )
            row = i // 3
            col = i % 3
            app_button.grid(row=row, column=col, padx=8, pady=8)
    
    def _setup_bottom_section(self):
        """Setup bottom section with theme colors."""
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        bottom_frame.pack(fill="x", padx=20, pady=10)
        
        # User profile
        user_label = ctk.CTkLabel(
            bottom_frame,
            text="👤 User",
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme.get_color("text_primary")
        )
        user_label.pack(side="left", padx=5)
        
        # Power button
        power_button = ctk.CTkButton(
            bottom_frame,
            text="⏻",
            width=40,
            height=35,
            fg_color="#E53935",
            text_color="white",
            hover_color="#C62828",
            corner_radius=8,
            command=self._show_power_options
        )
        power_button.pack(side="right", padx=5)
    
    def _filter_apps(self, event=None):
        """Filter apps based on search."""
        query = self.search.get().lower()
        for widget in self.apps_frame.winfo_children():
            if widget.winfo_class() == "CTkButton":
                text = widget.cget("text").lower()
                if query in text:
                    widget.grid()
                else:
                    widget.grid_remove()
    
    def _launch_app(self, app_name: str):
        """Launch application."""
        self.window_manager.kernel.process_manager.start_process(app_name)
        self.hide()
    
    def _show_power_options(self):
        """Show power options."""
        print("Power options: Shutdown, Restart, Sleep")
    
    def show(self):
        """Show start menu."""
        self.place(x=20, y=80)
    
    def hide(self):
        """Hide start menu."""
        self.place_forget()