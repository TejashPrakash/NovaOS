from sdk.command import NovaCommand


class OpenAppCommand(NovaCommand):

    NAME = "open_app"

    DESCRIPTION = "Launch an application"

    def execute(self, kernel, app_name):

        process = kernel.process_manager.start_process(app_name)

        return process is not None


class CloseAppCommand(NovaCommand):

    NAME = "close_app"

    DESCRIPTION = "Close a running application"

    def execute(self, kernel, app_name):

        if kernel.process_manager.get_process(app_name) is None:
            return False

        kernel.process_manager.stop_process(app_name)

        return True


class ListAppsCommand(NovaCommand):

    NAME = "list_apps"

    DESCRIPTION = "List installed applications and which ones are running"

    def execute(self, kernel):

        from apps.registry import APP_REGISTRY

        running = {
            process.name
            for process in kernel.process_manager.get_processes()
        }

        return {
            "installed": sorted(APP_REGISTRY),
            "running": sorted(running),
        }