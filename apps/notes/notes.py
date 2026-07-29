from core.base_app import BaseApp

import customtkinter as ctk


class NotesApp(BaseApp):

    APP_NAME = "Notes"

    APP_ICON = "📝"

    def __init__(self, window):

        super().__init__(window)

    def build(self):

        label = ctk.CTkLabel(
            self.content,
            text="Notes Coming Soon",
            font=("Segoe UI", 24, "bold")
        )

        label.pack(expand=True)