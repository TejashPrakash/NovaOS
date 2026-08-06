import customtkinter as ctk


class NotesToolbar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            height=50,
            fg_color="#252B3B"
        )

        self.pack_propagate(False)

        self.new_btn = ctk.CTkButton(
            self,
            text="New",
            width=90
        )

        self.new_btn.pack(
            side="left",
            padx=10,
            pady=8
        )

        self.save_btn = ctk.CTkButton(
            self,
            text="Save",
            width=90
        )

        self.save_btn.pack(
            side="left",
            padx=5
        )

        self.delete_btn = ctk.CTkButton(
            self,
            text="Delete",
            width=90,
            fg_color="#C62828",
            hover_color="#B71C1C"
        )

        self.delete_btn.pack(
            side="left",
            padx=5
        )

        self.status = ctk.CTkLabel(
            self,
            text="Ready"
        )

        self.status.pack(
            side="right",
            padx=15
        )

    # =====================================

    def set_status(self, text):

        self.status.configure(
            text=text
        )