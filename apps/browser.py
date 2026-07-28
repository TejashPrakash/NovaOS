import customtkinter as ctk


class BrowserApp:

    @staticmethod
    def build(window):

        label = ctk.CTkLabel(
            window.content,
            text="🌐 Nova Browser",
            font=("Segoe UI", 28, "bold")
        )

        label.pack(
            pady=40
        )