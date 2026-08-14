import customtkinter as ctk
from datetime import datetime


class Clock:
    """Enhanced clock widget with date display."""
    
    def __init__(self, parent):
        self.label = ctk.CTkLabel(
            parent,
            font=("Segoe UI", 12, "bold"),
            text_color="#00E5FF"
        )
        self.label.pack(
            pady=18
        )
        self.update()
        
    def update(self):
        """Update time and date display."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%a, %b %d")
        self.label.configure(
            text=f"{time_str}\n{date_str}"
        )
        self.label.after(
            1000,
            self.update
        )