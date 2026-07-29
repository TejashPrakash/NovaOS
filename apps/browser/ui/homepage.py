import customtkinter as ctk


class BrowserHome(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#151A24",
            corner_radius=12
        )

        # ===============================
        # Title
        # ===============================

        title = ctk.CTkLabel(
            self,
            text="🌐 Nova Browser",
            font=("Segoe UI", 32, "bold")
        )

        title.pack(pady=(60, 10))

        # ===============================
        # Subtitle
        # ===============================

        subtitle = ctk.CTkLabel(
            self,
            text="Fast • Modern • Integrated with NovaOS",
            font=("Segoe UI", 16),
            text_color="#BBBBBB"
        )

        subtitle.pack()

        # ===============================
        # Search Box
        # ===============================

        self.search = ctk.CTkEntry(
            self,
            width=500,
            height=45,
            placeholder_text="Search the web..."
        )

        self.search.pack(pady=35)

        # ===============================
        # Coming Soon
        # ===============================

        info = ctk.CTkLabel(
            self,
            text="Web Engine Coming Soon",
            font=("Segoe UI", 14),
            text_color="#777777"
        )

        info.pack()