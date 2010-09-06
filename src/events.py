class NoEventException(Exception):
    """Exception thrown if the event was not registered.
    Occurs only in strict mode."""

    def __init__(self, event_id, listener):
        self.event_id = event_id
        self.listener = listener

    def __str__(self):
        return "NoEventException: %s for %s" % (self.listener, self.event_id)

class MultipleRegistrationException(Exception):
    """Exception thrown if the event was already registered"""

    def __init__(self, event_id, emitter):
        self.event_id = event_id
        self.emitter = emitter

    def __str__(self):
        return "MultipleRegistrationException: %s on %s" % (self.event_id, emitter)

# TODO: use glib?
class EventEmitter:
    """Base class managing and emitting events"""

    def __init__(self, strict=True):
        """Using strict mode expects all events to be registered"""
        self._strict = strict
        self._listeners = {}

    def emit(self, event_id, *args):
        """Emit the event aka call all listeners with the given arguments"""
        listeners = self._listeners

        if event_id in listeners:
            for listener in listeners[event_id]:
                listener(*args)

    def listen(self, event_id, listener):
        """Add listener to the list of function which are called on the event"""
        listeners = self._listeners

        if event_id not in listeners:
            if self._strict:
                raise NoEventException(event_id, listener)
            else:
                register(event_id)

        listeners[event_id].append(listener)

    def register(self, event_id):
        """Add the event_id to the list of available events"""
        listeners = self._listeners

        if event_id not in listeners:
            listeners[event_id] = []
        else:
            # duplicated event ids should be detectet
            if self._strict:
                raise MultipleRegistrationException(event_id, self)

    def list_events(self):
        return self._listeners.keys()

