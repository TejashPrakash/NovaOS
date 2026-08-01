from sdk.command import NovaCommand


class OpenAppCommand(NovaCommand):

    NAME = "open_app"

    DESCRIPTION = "Launch an application"

    def execute(self, kernel, app_name):

        kernel.process_manager.start_process(app_name)

        return True