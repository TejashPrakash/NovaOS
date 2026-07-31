from datetime import datetime
import uuid


class Process:
    """
    Represents a running NovaOS application.
    """

    def __init__(self, app_name, app_class):

        # -----------------------------
        # Identity
        # -----------------------------

        self.pid = uuid.uuid4().hex[:8].upper()

        self.name = app_name

        self.app_class = app_class

        # -----------------------------
        # Runtime
        # -----------------------------

        self.window = None

        self.instance = None

        self.status = "Created"

        self.start_time = None

        # -----------------------------
        # Statistics (placeholder)
        # -----------------------------

        self.cpu_usage = 0.0

        self.memory_usage = 0.0

        self.thread_count = 1

    # =====================================================

    def start(self):

        self.status = "Running"

        self.start_time = datetime.now()

    # =====================================================

    def suspend(self):

        self.status = "Suspended"

    # =====================================================

    def resume(self):

        self.status = "Running"

    # =====================================================

    def terminate(self):

        self.status = "Terminated"

    # =====================================================

    def __repr__(self):

        return f"<Process {self.pid} | {self.name} | {self.status}>"