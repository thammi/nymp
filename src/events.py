##############################################################################
##
##  nymp - a graphical xmms2 cli frontend
##  Copyright 2010 Thammi
##
##  nymp is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  nymp is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with nymp.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

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

