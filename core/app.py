import customtkinter as ctk

from core.kernel import Kernel
from core.desktop import Desktop
from core.desktop_icons import DesktopIconsManager
from core.context_menu import ContextMenuManager
from core.dock import Dock
from core.window_manager import WindowManager
from core.launcher import Launcher
from core.start_menu import StartMenu


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

        self.context_menu_manager = ContextMenuManager(self.desktop)

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
            self.dock,
            self.kernel     
        )

        self.kernel.window_manager = self.window_manager

        # Register as a kernel service
        self.kernel.register_service(
            "window_manager",
            self.window_manager
        )

        self.kernel.register_service(
            "desktop",
            self.desktop
        )

        self.kernel.register_service(
            "dock",
            self.dock
        )

        # ==========================================
        # Desktop Icons
        # ==========================================

        self.desktop.icons_manager = DesktopIconsManager(
            self.desktop,
            self.window_manager
        )

        # ==========================================
        # Launcher
        # ==========================================

        self.launcher = Launcher(
            self.root,
            self.kernel
        )

        self.dock.set_launcher(self.launcher)

        # ==========================================
        # Start Menu
        # ==========================================

        self.start_menu = StartMenu(
            self.desktop.get_widget_layer(),
            self.window_manager
        )

        # Add start button to dock
        self.dock.add_start_button()

        # ==========================================
        # Global Events
        # ==========================================

        self.desktop.get_canvas().bind(
            "<Button-1>",
            lambda e: self.launcher.hide()
        )

        # Add AI panel toggle button to desktop
        def toggle_ai():
            """Safe toggle function that handles AI availability."""
            if hasattr(self.kernel, 'ai') and self.kernel.ai and getattr(self.kernel.ai, 'assistant', None):
                self.desktop.toggle_ai_panel(self.kernel.ai.assistant)
            else:
                print("[NovaOS] AI assistant not available")

        ai_toggle = ctk.CTkButton(
            self.desktop.get_widget_layer(),
            text="◈ Nova",
            width=100,
            height=35,
            fg_color="#00E5FF",
            text_color="black",
            hover_color="#00C8E8",
            corner_radius=8,
            command=toggle_ai
        )
        ai_toggle.place(x=1400, y=20)

        self.root.bind_all(
            "<Control-space>",
            lambda e: self.launcher.toggle()
        )

        print("[NovaOS] System Ready")

    # ==========================================

    def run(self):

        self.root.mainloop()