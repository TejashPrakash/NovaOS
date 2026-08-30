"""Keyboard shortcuts overlay for NovaOS — shows all available shortcuts."""

import customtkinter as ctk


class ShortcutsOverlay(ctk.CTkToplevel):
    """Full-screen overlay showing all keyboard shortcuts."""

    SHORTCUTS = [
        ("Launcher", [
            ("Ctrl+Space", "Toggle AI Launcher"),
            ("Ctrl+K", "AI Desktop Search"),
            ("Ctrl+D", "Demo Mode"),
            ("Ctrl+/", "Show This Overlay"),
        ]),
        ("Window Management", [
            ("Ctrl+Q", "Close Active Window"),
            ("Ctrl+Shift+L", "Lock Screen"),
            ("Ctrl+1/2/3/4", "Switch Virtual Desktop"),
        ]),
        ("Browser", [
            ("Enter", "Navigate to URL"),
            ("Mouse Wheel", "Scroll Page"),
            ("↑/↓", "Scroll Up/Down"),
        ]),
        ("Terminal", [
            ("Enter", "Execute Command"),
            ("↑/↓", "Command History"),
            ("Tab", "Auto-complete"),
            ("Tab Tab", "Show Completions"),
        ]),
        ("Notes", [
            ("Ctrl+S", "Save Note"),
            ("Ctrl+N", "New Note"),
        ]),
    ]

    def __init__(self, master):
        super().__init__(master)

        self.overrideredirect(True)
        self.configure(fg_color="#0A0E14EE")
        self.attributes("-topmost", True)

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        w, h = 650, 500
        self.geometry(f"{w}+{(screen_w - w) // 2}+{(screen_h - h) // 2}")

        self._build_ui()
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Control-slash>", lambda e: self.destroy())

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(header, text="⌨  Keyboard Shortcuts",
            font=("Segoe UI", 20, "bold"), text_color="#00E5FF"
        ).pack(side="left")

        ctk.CTkButton(header, text="✕", width=30, height=30,
            fg_color="transparent", text_color="#555555",
            hover_color="#161B22", corner_radius=15,
            command=self.destroy
        ).pack(side="right")

        # Shortcuts list
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        for section, shortcuts in self.SHORTCUTS:
            # Section header
            ctk.CTkLabel(scroll, text=section,
                font=("Segoe UI", 13, "bold"), text_color="#7B61FF"
            ).pack(anchor="w", pady=(10, 4))

            for key, desc in shortcuts:
                row = ctk.CTkFrame(scroll, fg_color="#161B22", corner_radius=6, height=32)
                row.pack(fill="x", pady=1)
                row.pack_propagate(False)

                # Key badge
                key_label = ctk.CTkLabel(row, text=f"  {key}  ",
                    font=("Cascadia Code", 11, "bold"), text_color="#00E5FF",
                    fg_color="#0D1117", corner_radius=4, width=150)
                key_label.pack(side="left", padx=(8, 12), pady=4)

                # Description
                ctk.CTkLabel(row, text=desc,
                    font=("Segoe UI", 11), text_color="#BBBBBB"
                ).pack(side="left", pady=4)

        # Footer
        ctk.CTkLabel(self, text="Press Escape or Ctrl+/ to close",
            font=("Segoe UI", 10), text_color="#555555"
        ).pack(pady=(0, 10))
