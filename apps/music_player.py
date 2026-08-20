import customtkinter as ctk
from sdk.app import NovaApp
from core.theme import ThemeManager


class MusicPlayerApp(NovaApp):
    APP_NAME = "Music Player"
    APP_ICON = "🎵"
    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 400
    
    def __init__(self, window):
        super().__init__(window)
        self.theme = ThemeManager()
    
    def build(self):
        # Premium music player UI
        label = ctk.CTkLabel(
            self.window.content,
            text="🎵 Nova Music\nComing Soon",
            font=("Segoe UI", 24, "bold"),
            text_color=self.theme.get_color("primary")
        )
        label.pack(expand=True)