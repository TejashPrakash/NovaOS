import customtkinter as ctk


class MusicPlayerApp:

    @staticmethod
    def build(window):

        label = ctk.CTkLabel(
            window.content,
            text="🎵 Nova Music\nComing Soon",
            font=("Segoe UI", 24, "bold")
        )

        label.pack(expand=True)