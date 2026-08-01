class ServiceContainer:

    def __init__(self):

        self._services = {}

    # =====================================

    def register(self, name, service):

        self._services[name] = service

    # =====================================

    def get(self, name):

        return self._services.get(name)

    # =====================================

    def exists(self, name):

        return name in self._services

    # =====================================

    def unregister(self, name):

        if name in self._services:
            del self._services[name]

    # =====================================

    def all(self):

        return self._services