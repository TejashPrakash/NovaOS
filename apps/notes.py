import customtkinter as ctk


class NotesApp:

    @staticmethod
    def build(window):

        textbox = ctk.CTkTextbox(
            window.content
        )

        textbox.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )