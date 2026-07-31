import customtkinter as ctk


class BrowserStatusBar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=28,
            fg_color="#222834",
            corner_radius=8
        )

        self.pack_propagate(False)

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            padx=10
        )

    # =======================================

    def set_status(self, text):

        self.status.configure(text=text)