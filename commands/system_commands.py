from sdk.command import NovaCommand


class ShutdownCommand(NovaCommand):

    NAME = "shutdown"

    DESCRIPTION = "Shutdown NovaOS"

    def execute(self, kernel):

        kernel.shutdown()

        return True