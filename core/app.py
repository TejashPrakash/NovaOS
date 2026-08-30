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
from core.demo_mode import DemoMode
from ai.ui.smart_hub import SmartSuggestionsWidget
from ai.ui.smart_notifications import SmartNotificationManager
from ai.ui.ai_search import AISearchDialog
from ai.ui.ai_context_menu import AIContextMenu


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
        # Full screen
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_w}x{screen_h}+0+0")
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
        self.dock.set_kernel(self.kernel)

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

        # AI toggle is now handled by the collapsible AI widget orb

        try:
            from ai.ui.desktop_widget import AIAssistantWidget
            if hasattr(self.kernel, 'ai') and self.kernel.ai and self.kernel.ai.assistant:
                self.ai_widget = AIAssistantWidget(
                    self.desktop.get_widget_layer(),
                    self.kernel.ai.assistant
                )
                # Right-center: avoids dock (bottom), system tray (bottom-right), icons (top-right)
                self.ai_widget.place(relx=1.0, rely=0.55, anchor="e", x=-20)
                self.ai_widget.lift()
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

        # Demo mode shortcut (Ctrl+D)
        def open_demo(e=None):
            DemoMode(self.root, kernel=self.kernel)

        self.root.bind_all("<Control-d>", open_demo)

        # Keyboard shortcuts overlay (Ctrl+/)
        def open_shortcuts(e=None):
            from core.shortcuts_overlay import ShortcutsOverlay
            ShortcutsOverlay(self.root)

        self.root.bind_all("<Control-slash>", open_shortcuts)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self._shutdown
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
        self.system_tray.lift()

        # ==========================================
        # AI Smart Hub (left side)
        # ==========================================
        try:
            self.smart_hub = SmartSuggestionsWidget(
                self.desktop.get_widget_layer(),
                kernel=self.kernel,
                on_toggle=self.desktop.on_smart_hub_toggle
            )
            self.smart_hub.place(x=20, y=20)
            self.smart_hub.lift()
        except Exception as e:
            print(f"[NovaOS] Smart Hub not available: {e}")

        # ==========================================
        # Smart AI Notifications
        # ==========================================
        try:
            self.smart_notifications = SmartNotificationManager(
                self.desktop, self.kernel
            )
            # Check for smart notifications every 5 minutes
            self.root.after(300000, self._check_smart_notifications)
            self._check_smart_notifications()
        except Exception as e:
            print(f"[NovaOS] Smart notifications not available: {e}")

        # ==========================================
        # Virtual Desktops (inline in dock)
        # ==========================================
        try:
            self.dock.virtual_desktops.kernel = self.kernel
            self.virtual_desktops = self.dock.virtual_desktops
        except Exception as e:
            print(f"[NovaOS] Virtual desktops not available: {e}")

        # ==========================================
        # AI Desktop Search (Ctrl+K)
        # ==========================================
        def open_ai_search(e=None):
            AISearchDialog(self.root, kernel=self.kernel)

        self.root.bind_all("<Control-k>", open_ai_search)

        # ==========================================
        # AI Context Menu on Desktop
        # ==========================================
        def show_ai_context(e=None):
            AIContextMenu(self.root, kernel=self.kernel)

        # Bind right-click to root so it catches ALL desktop clicks
        self.root.bind("<Button-3>", show_ai_context)

        # Keyboard shortcuts
        self.root.bind_all("<Control-1>", lambda e: self._switch_workspace(0))
        self.root.bind_all("<Control-2>", lambda e: self._switch_workspace(1))
        self.root.bind_all("<Control-3>", lambda e: self._switch_workspace(2))
        self.root.bind_all("<Control-4>", lambda e: self._switch_workspace(3))

        print("[NovaOS] System Ready")

    def _switch_workspace(self, index):
        """Switch to a virtual desktop workspace."""
        try:
            if hasattr(self, 'virtual_desktops'):
                self.virtual_desktops.switch_to(index)
        except Exception:
            pass

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

    def _check_smart_notifications(self):
        """Check and display smart notifications."""
        try:
            if hasattr(self, 'smart_notifications'):
                self.smart_notifications.check_and_notify()
        except Exception:
            pass
        self.root.after(300000, self._check_smart_notifications)

    # ==========================================

    def _shutdown(self):
        """Clean shutdown of NovaOS."""
        # Stop Playwright Chromium browser if running
        try:
            if hasattr(self, 'kernel') and self.kernel:
                wm = self.kernel.get_service("window_manager")
                if wm and hasattr(wm, 'windows'):
                    for window in wm.windows:
                        app = getattr(window, 'app', None)
                        if app:
                            for attr in ('chromium_engine', 'engine'):
                                eng = getattr(app, attr, None)
                                if eng and hasattr(eng, 'stop'):
                                    try:
                                        eng.stop()
                                    except Exception:
                                        pass
        except Exception:
            pass
        try:
            self.kernel.shutdown()
        except Exception:
            pass
        try:
            self.root.quit()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass

    def run(self):

        self.root.mainloop()