import customtkinter as ctk


class FileManagerApp:

    @staticmethod
    def build(window):

        label = ctk.CTkLabel(
            window.content,
            text="📁 File Manager Coming Soon",
            font=("Segoe UI", 24)
        )

        label.pack(
            expand=True
        )