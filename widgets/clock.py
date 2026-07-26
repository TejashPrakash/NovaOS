import customtkinter as ctk
from datetime import datetime


class Clock(ctk.CTkLabel):

    def __init__(self, master):

        super().__init__(
            master,
            text="",
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )

        self.update_clock()

    def update_clock(self):

        current_time = datetime.now().strftime("%I:%M:%S %p")

        self.configure(
            text=current_time
        )

        self.after(
            1000,
            self.update_clock
        )