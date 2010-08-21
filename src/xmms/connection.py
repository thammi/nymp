import xmmsclient
from xmmsclient import XMMS
from xmmsclient.glib import GLibConnector

from os.path import join

from events import EventEmitter

from player import Player
from playlist import Playlist

# TODO: think of a cool name
_ID = 'INSERT_NAME_HERE'

class XmmsConnection(EventEmitter):
    """Represantation of a XMMS connection. Use the modules (player)."""

    CONNECT_EVENT = "connect"
    DISCONNECT_EVENT = "disconnect"

    def __init__(self):
        EventEmitter.__init__(self)

        self.connected = False
        self.xmms = None

        # create events
        self.register(self.CONNECT_EVENT)
        self.register(self.DISCONNECT_EVENT)

        # initialize modules
        self.player = Player(self)
        self.playlist = Playlist(self)

    def connect(self):
        """Connect to a XMMS server"""
        if not self.connected:
            # disconnection callback
            def disconnected(r):
                self.connected = False
                self.xmms = None
                self.emit(self.DISCONNECT_EVENT)

            try:
                xmms = self.xmms = XMMS(_ID)

                # TODO: use path conventions
                xmms.connect(disconnect_func=disconnected)
                GLibConnector(xmms)
            except IOError:
                self.xmms = None
                self.connected = False
            else:
                self.connected = True
                self.emit(self.CONNECT_EVENT)

        return self.connected

