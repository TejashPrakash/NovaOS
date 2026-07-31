import customtkinter as ctk


class BrowserHomepage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        # ==========================================
        # Title
        # ==========================================

        title = ctk.CTkLabel(
            self,
            text="Nova Browser",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            pady=(70, 15)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Fast • Modern • Private",
            font=("Segoe UI", 16),
            text_color="gray"
        )

        subtitle.pack()

        # ==========================================
        # Search Box
        # ==========================================

        self.search = ctk.CTkEntry(
            self,
            width=500,
            height=42,
            placeholder_text="Search the web..."
        )

        self.search.pack(
            pady=(40, 15)
        )

        # ==========================================
        # Search Button
        # ==========================================

        self.search_btn = ctk.CTkButton(
            self,
            text="Search",
            width=140
        )

        self.search_btn.pack(
            pady=(0, 30)
        )

        # ==========================================
        # Bookmarks
        # ==========================================

        self.bookmarks_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.bookmarks_frame.pack(
            pady=10
        )

    # =====================================================

    def load_bookmarks(self, bookmarks, callback):

        for widget in self.bookmarks_frame.winfo_children():
            widget.destroy()

        for bookmark in bookmarks:

            button = ctk.CTkButton(
                self.bookmarks_frame,
                text=bookmark["title"],
                width=130,
                command=lambda b=bookmark: callback(b)
            )

            button.pack(
                side="left",
                padx=6
            )