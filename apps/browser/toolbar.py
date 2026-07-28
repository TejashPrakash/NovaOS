import customtkinter as ctk


class BrowserToolbar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=55,
            corner_radius=12,
            fg_color="#222834"
        )

        self.pack_propagate(False)

        # ---------------------------
        # Back
        # ---------------------------

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

        # ---------------------------
        # Forward
        # ---------------------------

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

        # ---------------------------
        # Refresh
        # ---------------------------

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

        # ---------------------------
        # Address Bar
        # ---------------------------

        self.address = ctk.CTkEntry(
            self,
            placeholder_text="Search Google or enter URL..."
        )

        self.address.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        # ---------------------------
        # Go
        # ---------------------------

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