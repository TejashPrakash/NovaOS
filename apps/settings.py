import customtkinter as ctk


class SettingsApp:

    @staticmethod
    def build(window):

        label = ctk.CTkLabel(
            window.content,
            text="⚙ Settings Coming Soon",
            font=("Segoe UI", 24)
        )

        label.pack(
            expand=True
        )