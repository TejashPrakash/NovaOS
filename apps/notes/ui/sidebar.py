import customtkinter as ctk


class NotesSidebar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=260,
            fg_color="#20242E"
        )

        self.pack_propagate(False)

        self.on_select = None
        self._all_notes = []

        self.buttons = []

        self.header = ctk.CTkLabel(
            self,
            text="Notes",
            font=("Segoe UI", 20, "bold")
        )

        self.header.pack(
            pady=(20, 5)
        )

        # Search bar
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="🔍 Search notes...",
            height=32,
            fg_color="#161B22",
            text_color="#FFFFFF",
            corner_radius=8,
            border_width=1,
            border_color="#333333",
            font=("Segoe UI", 12)
        )
        self.search_entry.pack(fill="x", padx=10, pady=(5, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search)

        self.notes_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.notes_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    # =====================================

    def set_callback(self, callback):
        """Set the callback for note selection."""
        self.on_select = callback

    def load_notes(self, notes):
        self._all_notes = notes
        self._render_notes(notes)

    def _render_notes(self, notes):
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        for note in notes:
            button = ctk.CTkButton(
                self.notes_frame,
                text=note["title"],
                anchor="w",
                height=40,
                command=lambda n=note["id"]: self.select(n)
            )
            button.pack(fill="x", pady=4)
            self.buttons.append(button)

    def _on_search(self, event=None):
        query = self.search_entry.get().strip().lower()
        if not query:
            self._render_notes(self._all_notes)
            return
        filtered = [n for n in self._all_notes if query in n.get("title", "").lower()]
        self._render_notes(filtered)

    # =====================================

    def select(self, note):

        if self.on_select:

            self.on_select(note)