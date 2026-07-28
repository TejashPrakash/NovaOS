import customtkinter as ctk

from core.desktop import Desktop
from core.dock import Dock
from core.window_manager import WindowManager
from core.launcher import Launcher


class NovaOS:

    def __init__(self):

        # ==========================================
        # Main Window
        # ==========================================

        self.root = ctk.CTk()

        self.root.title("NovaOS")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # ==========================================
        # Core Components
        # ==========================================

        self.desktop = Desktop(self.root)

        self.dock = Dock(self.root)

        self.window_manager = WindowManager(
            self.desktop,
            self.dock
        )

        self.launcher = Launcher(
            self.root,
            self.window_manager
        )

        self.dock.set_launcher(
            self.launcher
        )

        # ==========================================
        # Global Events
        # ==========================================

        # Clicking the desktop hides the launcher
        self.desktop.get_canvas().bind(
            "<Button-1>",
            lambda e: self.launcher.hide()
        )

        # Ctrl + Space toggles the launcher
        self.root.bind_all(
            "<Control-space>",
            lambda e: self.launcher.toggle()
        )

    def run(self):

        self.root.mainloop()