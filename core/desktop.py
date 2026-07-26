import customtkinter as ctk

from core.taskbar import Taskbar


class Desktop(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("NovaOS")
        self.geometry("1600x900")
        self.minsize(1200, 700)

        self.configure(fg_color="#0D1117")

        # Desktop background
        self.desktop = ctk.CTkFrame(
            self,
            fg_color="#0D1117",
            corner_radius=0
        )
        self.desktop.pack(fill="both", expand=True)

        # Desktop title
        title = ctk.CTkLabel(
            self.desktop,
            text="NovaOS",
            font=("Segoe UI", 32, "bold"),
            text_color="#00E5FF"
        )

        title.place(x=30, y=20)

        subtitle = ctk.CTkLabel(
            self.desktop,
            text="The Future of Personal Computing",
            font=("Segoe UI", 14),
            text_color="#BBBBBB"
        )

        subtitle.place(x=35, y=65)

        # Taskbar
        self.taskbar = Taskbar(self)