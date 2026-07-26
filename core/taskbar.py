import customtkinter as ctk
from datetime import datetime


class Taskbar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            height=60,
            fg_color="#161B22",
            corner_radius=0
        )

        self.pack(side="bottom", fill="x")

        # Start button
        self.start_btn = ctk.CTkButton(
            self,
            text="◈ Nova",
            width=110,
            height=40,
            fg_color="#00E5FF",
            text_color="black",
            hover_color="#00C8E8"
        )

        self.start_btn.pack(side="left", padx=15, pady=10)

        # Spacer
        self.center = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.center.pack(side="left", expand=True)

        # Clock
        self.clock = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 14)
        )

        self.clock.pack(side="right", padx=20)

        self.update_clock()

    def update_clock(self):
        now = datetime.now().strftime("%I:%M:%S %p")
        self.clock.configure(text=now)
        self.after(1000, self.update_clock)