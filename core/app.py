import customtkinter as ctk

from core.kernel import Kernel
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
        # Kernel
        # ==========================================

        self.kernel = Kernel()

        self.kernel.boot()

        # ==========================================
        # Desktop
        # ==========================================

        self.desktop = Desktop(self.root)

        self.kernel.desktop = self.desktop

        # ==========================================
        # Dock
        # ==========================================

        self.dock = Dock(self.root)

        self.kernel.dock = self.dock

        # ==========================================
        # Window Manager
        # ==========================================

        self.window_manager = WindowManager(
            self.desktop,
            self.dock
        )

        self.kernel.window_manager = self.window_manager

        # ==========================================
        # Launcher
        # ==========================================

        self.launcher = Launcher(
            self.root,
            self.kernel
        )

        self.dock.set_launcher(
            self.launcher
        )

        # ==========================================
        # Global Events
        # ==========================================

        self.desktop.get_canvas().bind(
            "<Button-1>",
            lambda e: self.launcher.hide()
        )

        self.root.bind_all(
            "<Control-space>",
            lambda e: self.launcher.toggle()
        )

        print("[NovaOS] System Ready")

    # =====================================================

    def run(self):

        self.root.mainloop()