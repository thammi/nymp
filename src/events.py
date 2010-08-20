class NoEventException(Exception):

    def __init__(self, event_id, listener):
        self.event_id = event_id
        self.listener = listener

    def __str__(self):
        return "NoEventException: %s for %s" % (self.listener, self.event_id)

# TODO: use glib?
class EventEmitter:

    def __init__(self, demand_registration=True):
        self.strict = demand_registration
        self.listeners = {}

    def emit(self, event_id, *args):
        listeners = self.listeners

        if event_id in listeners:
            for listener in listeners[event_id]:
                listener(*args)

    def listen(self, event_id, listener):
        listeners = self.listeners

        if event_id not in listeners:
            if self.strict:
                raise NoEventException(event_id, listener)
            else:
                register(event_id)

        listeners[event_id].append(listener)

    def register(self, event_id):
        listeners = self.listeners

        if event_id not in listeners:
            listeners[event_id] = []

