import customtkinter as ctk


class BrowserToolbar(ctk.CTkFrame):

    def __init__(self, parent, browser):

        super().__init__(
            parent,
            height=55,
            fg_color="#222834",
            corner_radius=12
        )

        self.browser = browser

        self.pack_propagate(False)

        self.back_btn = ctk.CTkButton(
            self,
            text="←",
            width=40,
            command=self.browser.back
        )

        self.back_btn.pack(side="left", padx=(10, 5), pady=10)

        self.forward_btn = ctk.CTkButton(
            self,
            text="→",
            width=40,
            command=self.browser.forward
        )

        self.forward_btn.pack(side="left", padx=5, pady=10)

        self.refresh_btn = ctk.CTkButton(
            self,
            text="⟳",
            width=40,
            command=self.browser.reload
        )

        self.refresh_btn.pack(side="left", padx=5, pady=10)

        self.address = ctk.CTkEntry(
            self,
            placeholder_text="Enter URL..."
        )

        self.address.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.address.bind(
            "<Return>",
            self.go
        )

        self.go_btn = ctk.CTkButton(
            self,
            text="Go",
            width=60,
            command=self.go
        )

        self.go_btn.pack(
            side="right",
            padx=10,
            pady=10
        )

    # ---------------------------------------

    def go(self, event=None):

        url = self.address.get().strip()

        if url:
            self.browser.load(url)