import customtkinter as ctk

from datetime import datetime


class Clock:

    def __init__(self, parent):

        self.label = ctk.CTkLabel(
            parent,
            font=("Segoe UI", 15, "bold")
        )

        self.label.pack(
            pady=22
        )

        self.update()

    def update(self):

        current = datetime.now().strftime("%I:%M %p")

        self.label.configure(
            text=current
        )

        self.label.after(
            1000,
            self.update
        )