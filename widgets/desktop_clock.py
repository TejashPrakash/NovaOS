"""Large floating clock widget for the NovaOS desktop."""

import customtkinter as ctk
from datetime import datetime
from core.theme import ThemeManager


class DesktopClock(ctk.CTkFrame):
    """Big transparent clock floating on the desktop — bottom-left area."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#0D1117",
            corner_radius=16,
            border_width=1,
            border_color="#1A2332",
            **kwargs
        )
        self.theme = ThemeManager()
        self.configure(width=220, height=110)
        self.pack_propagate(False)

        # Time
        self.time_label = ctk.CTkLabel(
            self,
            text="00:00",
            font=("Segoe UI", 36, "bold"),
            text_color="#00E5FF"
        )
        self.time_label.pack(pady=(12, 0))

        # Date
        self.date_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 12),
            text_color="#888888"
        )
        self.date_label.pack()

        # Day
        self.day_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 11, "bold"),
            text_color="#7B61FF"
        )
        self.day_label.pack(pady=(0, 8))

        self._tick()

    def _tick(self):
        now = datetime.now()
        self.time_label.configure(text=now.strftime("%I:%M:%S %p"))
        self.date_label.configure(text=now.strftime("%B %d, %Y"))
        self.day_label.configure(text=now.strftime("%A"))
        self.after(1000, self._tick)
