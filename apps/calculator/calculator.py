from core.base_app import BaseApp

import customtkinter as ctk


class CalculatorApp(BaseApp):

    APP_NAME = "Calculator"

    APP_ICON = "🧮"

    def __init__(self, window):

        super().__init__(window)

    def build(self):

        label = ctk.CTkLabel(
            self.content,
            text="Calculator Coming Soon",
            font=("Segoe UI", 24, "bold")
        )

        label.pack(expand=True)