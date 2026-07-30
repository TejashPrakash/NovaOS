import customtkinter as ctk


class BrowserToolbar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=55,
            fg_color="#222834",
            corner_radius=12
        )

        self.pack_propagate(False)

        # ==========================================
        # Back
        # ==========================================

        self.back_btn = ctk.CTkButton(
            self,
            text="←",
            width=40
        )

        self.back_btn.pack(
            side="left",
            padx=(10, 5),
            pady=10
        )

        # ==========================================
        # Forward
        # ==========================================

        self.forward_btn = ctk.CTkButton(
            self,
            text="→",
            width=40
        )

        self.forward_btn.pack(
            side="left",
            padx=5,
            pady=10
        )

        # ==========================================
        # Refresh
        # ==========================================

        self.refresh_btn = ctk.CTkButton(
            self,
            text="⟳",
            width=40
        )

        self.refresh_btn.pack(
            side="left",
            padx=5,
            pady=10
        )

        # ==========================================
        # Home
        # ==========================================

        self.home_btn = ctk.CTkButton(
            self,
            text="🏠",
            width=40
        )

        self.home_btn.pack(
            side="left",
            padx=5,
            pady=10
        )

        # ==========================================
        # Address Bar
        # ==========================================

        self.url_var = ctk.StringVar()

        self.url_entry = ctk.CTkEntry(
            self,
            textvariable=self.url_var
        )

        self.url_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        # ==========================================
        # Go Button
        # ==========================================

        self.go_btn = ctk.CTkButton(
            self,
            text="Go",
            width=60
        )

        self.go_btn.pack(
            side="right",
            padx=10,
            pady=10
        )

    # ==========================================

    def set_url(self, url):

        self.url_var.set(url)

    def get_url(self):

        return self.url_var.get()