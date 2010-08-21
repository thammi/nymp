import xmmsclient
from xmmsclient import XMMS, userconfdir_get
from xmmsclient.glib import GLibConnector

from os.path import join

from events import EventEmitter

# TODO: think of a cool name
_ID = 'INSERT_NAME_HERE'

def get_config_dir():
    """Get configuration directory according to XMMS2 guideline"""
    return join(userconfdir_get(), "clients", _ID)

def reduce_meta(meta):
    tuples = ((name, value) for (plugin, name), value in meta.items())
    return dict(tuples)


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


class Player(EventEmitter):
    """Player module. Control what is played how."""

    STATUS_EVENT = 'status_changed'
    VOLUME_EVENT = 'volume_changed'
    CURRENT_EVENT = 'current_changed'

    STATUS_PLAY = xmmsclient.PLAYBACK_STATUS_PLAY
    STATUS_PAUSE = xmmsclient.PLAYBACK_STATUS_PAUSE
    STATUS_STOP = xmmsclient.PLAYBACK_STATUS_PAUSE

    def __init__(self, connection):
        EventEmitter.__init__(self)

        self.connection = connection

        # create events
        self.register(self.STATUS_EVENT)
        self.register(self.VOLUME_EVENT)
        self.register(self.CURRENT_EVENT)

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
        status = self._status = value.value()
        self.emit(self.STATUS_EVENT, status)

    def _volume_change(self, value):
        self.emit(self.VOLUME_EVENT, value.value())

    def toggle(self):
        if self._status == self.STATUS_PLAY:
            self.pause()
        else:
            self.start()

    def pause(self):
        self.connection.xmms.playback_pause()

    def start(self):
        self.connection.xmms.playback_start()

    def stop(self):
        self.connection.xmms.playback_stop()

    def forward(self):
        self.connection.xmms.playback_tickle()

    # TODO: last()

    def set_volume(self, volume):
        self.connection.xmms.volume_set(volume)

