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

        btn_style = dict(width=40, height=30, corner_radius=6,
                         fg_color="#2B3340", hover_color="#3A4256",
                         font=("Segoe UI", 13))

        # Navigation buttons
        self.back_btn = ctk.CTkButton(self, text="←", **btn_style)
        self.back_btn.pack(side="left", padx=(10, 2), pady=12)

        self.forward_btn = ctk.CTkButton(self, text="→", **btn_style)
        self.forward_btn.pack(side="left", padx=2, pady=12)

        self.up_btn = ctk.CTkButton(self, text="↑", **btn_style)
        self.up_btn.pack(side="left", padx=2, pady=12)

        self.refresh_btn = ctk.CTkButton(self, text="⟳", **btn_style)
        self.refresh_btn.pack(side="left", padx=2, pady=12)

        # Separator
        ctk.CTkFrame(self, width=1, height=30, fg_color="#3A4256").pack(
            side="left", padx=8, pady=12)

        # File operation buttons
        op_style = dict(width=50, height=30, corner_radius=6,
                        fg_color="#2B3340", hover_color="#3A4256",
                        font=("Segoe UI", 11))

        self.paste_btn = ctk.CTkButton(self, text="📋 Paste", **op_style)
        self.paste_btn.pack(side="left", padx=2, pady=12)

        self.new_folder_btn = ctk.CTkButton(self, text="📁 New", **op_style)
        self.new_folder_btn.pack(side="left", padx=2, pady=12)

        # Path Bar
        self.path_var = ctk.StringVar()
        self.path_entry = ctk.CTkEntry(
            self, textvariable=self.path_var,
            fg_color="#1A1F2B", text_color="#CCCCCC",
            border_width=1, border_color="#333333"
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=10, pady=12)

    def set_path(self, path):
        self.path_var.set(str(path))