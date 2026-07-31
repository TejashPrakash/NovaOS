from core.process_manager import ProcessManager


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

        self.process_manager = ProcessManager(self)

        self.ai = None

        self.services = {}

        self.running = False

    # =====================================================

    def boot(self):

        print("[Kernel] Booting NovaOS...")

        self.running = True

    # =====================================================

    def shutdown(self):

        print("[Kernel] Shutting down NovaOS...")

        self.running = False

    # =====================================================

    def register_service(self, name, service):

        self.services[name] = service

    # =====================================================

    def get_service(self, name):

        return self.services.get(name)