import customtkinter as ctk

from core.desktop import Desktop
from core.dock import Dock
from core.window_manager import WindowManager


class NovaOS:

    def __init__(self):

        # -----------------------------
        # Main Window
        # -----------------------------

        self.root = ctk.CTk()

        self.root.title("NovaOS")

        self.root.geometry("1600x900")

        self.root.minsize(1200, 700)

        ctk.set_appearance_mode("Dark")

        ctk.set_default_color_theme("blue")

        # -----------------------------
        # Core Components
        # -----------------------------

        self.desktop = Desktop(self.root)

        self.dock = Dock(self.root)

        self.window_manager = WindowManager(
            self.desktop,
            self.dock
        )

        self.window_manager.create_window("Browser")

        self.window_manager.create_window("Notes")

    def run(self):

        self.root.mainloop()