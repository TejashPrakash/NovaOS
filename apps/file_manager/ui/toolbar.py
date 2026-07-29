import customtkinter as ctk


class FileToolbar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=55,
            fg_color="#222834",
            corner_radius=12
        )

        self.pack_propagate(False)

        # ======================================
        # Back
        # ======================================

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

        # ======================================
        # Forward
        # ======================================

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

        # ======================================
        # Up
        # ======================================

        self.up_btn = ctk.CTkButton(
            self,
            text="↑",
            width=40
        )

        self.up_btn.pack(
            side="left",
            padx=5,
            pady=10
        )

        # ======================================
        # Refresh
        # ======================================

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

        # ======================================
        # Path Bar
        # ======================================

        self.path_var = ctk.StringVar()

        self.path_entry = ctk.CTkEntry(
            self,
            textvariable=self.path_var
        )

        self.path_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

    # ======================================

    def set_path(self, path):

        self.path_var.set(str(path))