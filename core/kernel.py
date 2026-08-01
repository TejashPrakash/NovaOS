from core.process_manager import ProcessManager
from sdk.events import EventBus
from sdk.service import ServiceContainer
from services.ai_service import AIService
from services.audio_service import AudioService
from services.settings_service import SettingsService
from services.wallpaper_service import WallpaperService
from sdk.command import CommandRegistry

class Kernel:
    """
    NovaOS Kernel

    The Kernel is the heart of NovaOS.

    It owns and coordinates every major system:
        - Process Manager
        - Window Manager
        - Desktop
        - Dock
        - AI
        - Services
    """

    def __init__(self):

        self.desktop = None
        self.dock = None
        self.window_manager = None
        self.events = EventBus()
        self.process_manager = ProcessManager(self)

        self.ai = None

        self.services = ServiceContainer()
        self.plugins = []
        self.commands = CommandRegistry()

        self.running = False

    # =====================================================

    def boot(self):

        print("[Kernel] Booting NovaOS...")

        self.register_service("ai", AIService())
        self.register_service("audio", AudioService())
        self.register_service("settings", SettingsService())
        self.register_service("wallpaper", WallpaperService())
        self.register_service("process_manager", self.process_manager)

        self.running = True

    # =====================================================

    def shutdown(self):

        print("[Kernel] Shutting down NovaOS...")

        self.running = False

    # =====================================================

    def register_service(self, name, service):

        self.services.register(name, service)

    # =====================================================

    def get_service(self, name):

        return self.services.get(name)

    # =====================================================

    def load_plugin(self, plugin):

        plugin.on_load(self)

        self.plugins.append(plugin)

    # =====================================================

    def unload_plugin(self, plugin):

        plugin.on_unload(self)

        self.plugins.remove(plugin)