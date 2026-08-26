import customtkinter as ctk

from core.kernel import Kernel
from core.desktop import Desktop
from core.desktop_icons import DesktopIconsManager
from core.context_menu import ContextMenuManager
from core.notifications import NotificationSystem
from core.dock import Dock
from core.window_manager import WindowManager
from core.launcher import Launcher
from core.start_menu import StartMenu
from core.system_tray import SystemTray


class NovaOS:

    def __init__(self, root=None):

        # ==========================================
        # Main Window
        # ==========================================

        if root is not None:
            self.root = root
        else:
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

        self.notifications = NotificationSystem(self.desktop)

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

        self.desktop.window_manager = self.window_manager
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
            "notifications",
            self.notifications
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
        # Premium Effects Toggle
        # ==========================================
        self.premium_effects_enabled = False

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
        self.dock.add_start_button(self.start_menu)
        self.dock.integrate_launcher_with_start_menu()

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

        try:
            from ai.ui.desktop_widget import AIAssistantWidget
            if hasattr(self.kernel, 'ai') and self.kernel.ai and self.kernel.ai.assistant:
                self.ai_widget = AIAssistantWidget(
                    self.desktop.get_widget_layer(),
                    self.kernel.ai.assistant
                )
                self.ai_widget.place(relx=1.0, rely=0.5, anchor="e", x=-20)
        except Exception as e:
            print(f"[NovaOS] AI widget not available: {e}")

        self.root.bind_all(
            "<Control-space>",
            lambda e: self.launcher.toggle()
        )

        # Lock screen shortcut (Ctrl+Shift+L)
        def lock_screen():
            from core.lock_screen import LockScreen
            LockScreen(on_unlock=lambda: None)

        self.root.bind_all(
            "<Control-Shift-L>",
            lambda e: lock_screen()
        )

        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.kernel.commands.execute(self.kernel, "shutdown")
        )

        # ==========================================
        # System Tray
        # ==========================================
        self.system_tray = SystemTray(
            self.desktop.get_widget_layer(),
            kernel=self.kernel
        )
        self.system_tray.place(
            relx=1.0, rely=1.0, anchor="se",
            x=-15, y=-55
        )

        print("[NovaOS] System Ready")

    # ==========================================
    # Premium Effects
    # ==========================================

    def toggle_premium_effects(self):
        """Toggle premium visual effects."""
        self.premium_effects_enabled = not self.premium_effects_enabled
        
        if self.premium_effects_enabled:
            # Enable premium effects
            self.desktop.enable_neural_network_background()
            self.desktop.enable_ambient_lighting()
            print("[NovaOS] Premium effects enabled")
        else:
            # Disable premium effects
            self.desktop.disable_neural_network_background()
            self.desktop.disable_ambient_lighting()
            print("[NovaOS] Premium effects disabled")

    def set_theme(self, theme_name: str):
        """Apply theme to NovaOS."""
        self.desktop.set_theme(theme_name)
        print(f"[NovaOS] Theme changed to {theme_name}")

    # ==========================================

    def run(self):

        self.root.mainloop()