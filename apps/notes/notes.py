from sdk.app import NovaApp

import customtkinter as ctk


class NotesApp(NovaApp):

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