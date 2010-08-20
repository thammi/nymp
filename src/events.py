class NoEventException(Exception):
    pass

# TODO: use glib?
class EventEmitter:

    def __init__(self, demand_registration=True):
        self.strict = demand_registration
        self.listeners = {}

    def emit(event_id, *args):
        listeners = self.listeners

        if event_id in listeners:
            for listener in listeners[event_id]:
                listener(*args)

    def listen(event_id, listener):
        listeners = self.listeners

        if event_id not in listeners:
            if self.strict:
                raise NoEventException()
            else:
                register(event_id)

        listeners[event_id].append(listener)

    def register(event_id):
        listeners[event_id] = []

