from sdk.command import NovaCommand


class ShutdownCommand(NovaCommand):

    NAME = "shutdown"

    DESCRIPTION = "Shutdown NovaOS"

    def execute(self, kernel):
        kernel.shutdown()
        desktop = getattr(kernel, "desktop", None)
        if desktop is not None and getattr(desktop, "root", None) is not None:
            desktop.root.after(100, desktop.root.destroy)
        return True