class NovaCommand:

    NAME = "command"

    DESCRIPTION = ""

    def execute(self, kernel, *args, **kwargs):
        raise NotImplementedError()


class CommandRegistry:

    def __init__(self):

        self.commands = {}

    # =====================================

    def register(self, command):

        self.commands[command.NAME] = command

    # =====================================

    def execute(self, kernel, name, *args, **kwargs):

        if name not in self.commands:
            raise ValueError(f"Unknown command: {name}")

        return self.commands[name].execute(
            kernel,
            *args,
            **kwargs
        )

    # =====================================

    def get(self, name):

        return self.commands.get(name)

    # =====================================

    def all(self):

        return self.commands