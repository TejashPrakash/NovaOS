import customtkinter as ctk


class NotesEditor(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.title_entry = ctk.CTkEntry(
            self,
            height=40,
            placeholder_text="Title"
        )

        self.title_entry.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        self.text = ctk.CTkTextbox(
            self,
            font=("Consolas", 14)
        )

        self.text.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    # =====================================

    def set_title(self, title):
        """Set the title in the editor."""
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, title)

    def set_content(self, content):
        """Set the content in the editor."""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)

    def load_note(self, note):

        self.title_entry.delete(0, "end")
        self.title_entry.insert(
            0,
            note["title"]
        )

        self.text.delete(
            "1.0",
            "end"
        )

        self.text.insert(
            "1.0",
            note["content"]
        )

    # =====================================

    def clear(self):

        self.title_entry.delete(
            0,
            "end"
        )

        self.text.delete(
            "1.0",
            "end"
        )

    # =====================================

    def get_title(self):

        return self.title_entry.get()

    # =====================================

    def get_content(self):

        return self.text.get(
            "1.0",
            "end-1c"
        )