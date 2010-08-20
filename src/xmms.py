from xmmsclient import XMMS, userconfdir_get
from xmmsclient.glib import GLibConnector
from os.path import join

from events import EventEmitter

# TODO: think of a cool name
_ID = 'INSERT_NAME_HERE'

def get_config_dir():
    return join(userconfdir_get(), "clients", _ID)


class XmmsConnection(EventEmitter):

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

        self.connect()

    def connect(self):
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


class Player(EventEmitter):

    STATUS_EVENT = "status_changed"
    VOLUME_EVENT = "volume_changed"
    CURRENT_EVENT = "current_changed"

    def __init__(self, connection):
        EventEmitter.__init__(self)

        self.connection = connection

        connection.listen(connection.CONNECT_EVENT, self._connected)

    def _connected(self):
        xmms = self.connection.xmms

        # set callbacks
        xmms.broadcast_playback_current_id(self._current_change)
        xmms.broadcast_playback_status(self._status_change)
        xmms.broadcast_playback_volume_changed(self._volume_change)

        # get current data
        xmms.playback_current_id(cb=self._current_change)
        xmms.playback_status(cb=self._status_change)
        xmms.playback_volume_get(cb=self._volume_change)

    def _current_change(self, value):
        xmms = self.connection.xmms
        xmms.medialib_get_info(value.value(), cb=self._current_info)

    def _current_info(self, result):
        self.emit(self.CURRENT_EVENT, result.value())

    def _status_change(self, value):
        self.emit(self.STATUS_EVENT, value.value())

    def _volume_change(self, value):
        self.emit(self.VOLUME_EVENT, value.value())

