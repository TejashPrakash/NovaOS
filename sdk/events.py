class EventBus:

    def __init__(self):

        self.listeners = {}

    # =====================================

    def subscribe(self, event, callback):

        self.listeners.setdefault(
            event,
            []
        ).append(callback)

    # =====================================

    def unsubscribe(self, event, callback):

        if event in self.listeners:

            if callback in self.listeners[event]:

                self.listeners[event].remove(callback)

    # =====================================

    def emit(self, event, *args, **kwargs):

        for callback in self.listeners.get(event, []):

            callback(*args, **kwargs)