from apps.registry import APP_REGISTRY
from core.process import Process


class ProcessManager:
    """
    Manages every running process inside NovaOS.
    """

    def __init__(self, kernel):

        self.kernel = kernel

        self.processes = {}

    # =====================================================

    def start_process(self, app_name):

        # ---------------------------------
        # Already running?
        # ---------------------------------

        for pid, process in list(self.processes.items()):

            if process.name != app_name:
                continue

            # Window still exists
            if (
                process.window is not None
                and process.window.winfo_exists()
            ):
                process.window.focus_window()
                return process

            # Dead window -> remove process
            del self.processes[pid]
            break

        # ---------------------------------
        # Unknown app
        # ---------------------------------

        if app_name not in APP_REGISTRY:

            print(f"[ProcessManager] Unknown application: {app_name}")

            return None

        # ---------------------------------
        # Create Process
        # ---------------------------------

        process = Process(
            app_name,
            APP_REGISTRY[app_name]
        )

        process.start()

        # ---------------------------------
        # Create Window
        # ---------------------------------

        app_class = APP_REGISTRY[app_name]

        window = self.kernel.window_manager.create_window(
            app_name,
            width=app_class.DEFAULT_WIDTH,
            height=app_class.DEFAULT_HEIGHT,
            launch_app=False
        )

        process.window = window
        window.kernel = self.kernel
        window.app_name = app_name

        # ---------------------------------
        # Create App
        # ---------------------------------

        app = app_class(window)

        process.instance = app
        window.app = app

        app.build()

        # ---------------------------------
        # Register
        # ---------------------------------

        self.processes[process.pid] = process

        self.kernel.events.emit(
            "process_started",
            process
        )

        print(f"[Kernel] Started {app_name} ({process.pid})")

        return process

    # =====================================================

    def stop_process(self, app_name):

        """
        Stop process by application name.
        """

        for pid, process in list(self.processes.items()):

            if process.name != app_name:
                continue

            process.terminate()

            del self.processes[pid]

            self.kernel.events.emit(
                "process_stopped",
                process
            )

            print(f"[Kernel] Stopped {app_name} ({pid})")

            return

    # =====================================================

    def get_process(self, app_name):

        for process in self.processes.values():

            if process.name == app_name:
                return process

        return None

    # =====================================================

    def get_processes(self):

        return list(self.processes.values())