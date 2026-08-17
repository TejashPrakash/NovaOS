import customtkinter as ctk
from datetime import datetime
from core.theme import ThemeManager


class Clock:
    """Enhanced clock widget with theme integration."""
    
    def __init__(self, parent):
        self.theme = ThemeManager()
        self.label = ctk.CTkLabel(
            parent,
            font=("Segoe UI", 12, "bold"),
            text_color=self.theme.get_color("primary")
        )
        self.label.pack(pady=18)
        self.update()
    
    def update(self):
        """Update time and date display with theme colors."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%a, %b %d")
        
        self.label.configure(
            text=f"{time_str}\n{date_str}",
            text_color=self.theme.get_color("primary")
        )
        self.label.after(1000, self.update)