import customtkinter as ctk


class BrowserHome(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#151A24",
            corner_radius=12
        )

        title = ctk.CTkLabel(
            self,
            text="🌐 Nova Browser",
            font=("Segoe UI", 34, "bold")
        )

        title.pack(
            pady=(60, 10)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Welcome to NovaOS Browser",
            font=("Segoe UI", 18)
        )

        subtitle.pack()

        search = ctk.CTkEntry(
            self,
            width=500,
            height=45,
            placeholder_text="Search the web..."
        )

        search.pack(
            pady=35
        )