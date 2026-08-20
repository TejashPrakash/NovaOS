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

        self.buttons = []

        self.header = ctk.CTkLabel(
            self,
            text="Notes",
            font=("Segoe UI", 20, "bold")
        )

        self.header.pack(
            pady=(20, 15)
        )

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

            button.pack(
                fill="x",
                pady=4
            )

            self.buttons.append(button)

    # =====================================

    def select(self, note):

        if self.on_select:

            self.on_select(note)