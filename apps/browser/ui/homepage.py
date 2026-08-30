import customtkinter as ctk

class BrowserHomepage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        title = ctk.CTkLabel(self, text="Nova Browser", font=("Segoe UI", 30, "bold"))
        title.pack(pady=(70, 15))

        subtitle = ctk.CTkLabel(self, text="AI-Powered • Fast • Modern", font=("Segoe UI", 16), text_color="gray")
        subtitle.pack()

        self.search = ctk.CTkEntry(self, width=500, height=42, placeholder_text="Search the web...")
        self.search.pack(pady=(40, 15))

        self.search_btn = ctk.CTkButton(self, text="Search", width=140)
        self.search_btn.pack(pady=(0, 30))

        self.bookmarks_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bookmarks_frame.pack(pady=10)

    def load_bookmarks(self, bookmarks, on_open, on_delete=None):
        for widget in self.bookmarks_frame.winfo_children():
            widget.destroy()

        for bookmark in bookmarks:
            row = ctk.CTkFrame(self.bookmarks_frame, fg_color="transparent")
            row.pack(side="left", padx=4, pady=2)

            button = ctk.CTkButton(
                row,
                text=bookmark["title"],
                width=110,
                command=lambda b=bookmark: on_open(b)
            )
            button.pack(side="left")

            if on_delete:
                del_btn = ctk.CTkButton(
                    row, text="✕", width=24, height=24, corner_radius=12,
                    fg_color="transparent", text_color="#FF5252",
                    hover_color="#331111", font=("Segoe UI", 10),
                    command=lambda b=bookmark: on_delete(b)
                )
                del_btn.pack(side="left", padx=(2, 0))