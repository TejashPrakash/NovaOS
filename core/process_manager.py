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

        # -----------------------------
        # Already running?
        # -----------------------------

        for process in self.processes.values():

            if process.name == app_name:

                if process.window:
                    process.window.focus_window()

                return process

        # -----------------------------
        # Application exists?
        # -----------------------------

        if app_name not in APP_REGISTRY:

            print(f"[ProcessManager] Unknown application: {app_name}")

            return None

        # -----------------------------
        # Create Process
        # -----------------------------

        process = Process(
            app_name,
            APP_REGISTRY[app_name]
        )

        process.start()

        # -----------------------------
        # Create Window
        # -----------------------------

        window = self.kernel.window_manager.create_window(
            app_name,
            launch_app=False
        )

        process.window = window

        # -----------------------------
        # Create Application
        # -----------------------------

        app = APP_REGISTRY[app_name](window)

        process.instance = app

        window.app = app

        app.build()

        # -----------------------------
        # Register Process
        # -----------------------------

        self.processes[process.pid] = process

        print(f"[Kernel] Started {app_name} ({process.pid})")

        return process

    # =====================================================

    def stop_process(self, pid):

        if pid not in self.processes:
            return

        process = self.processes[pid]

        process.terminate()

        if process.window:
            self.kernel.window_manager.close_window(
                process.window
            )

        del self.processes[pid]

    # =====================================================

    def get_processes(self):

        return list(self.processes.values())