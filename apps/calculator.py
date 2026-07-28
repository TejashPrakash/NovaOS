import customtkinter as ctk


class CalculatorApp:

    @staticmethod
    def build(window):

        label = ctk.CTkLabel(
            window.content,
            text="🧮 Calculator Coming Soon",
            font=("Segoe UI", 24)
        )

        label.pack(
            expand=True
        )