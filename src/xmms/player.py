import xmmsclient

from events import EventEmitter
from helper import value_wrap

class Player(EventEmitter):
    """Control what is played how"""

    STATUS_EVENT = 'status_changed'
    VOLUME_EVENT = 'volume_changed'
    CURRENT_EVENT = 'current_changed'

    STATUS_PLAY = xmmsclient.PLAYBACK_STATUS_PLAY
    STATUS_PAUSE = xmmsclient.PLAYBACK_STATUS_PAUSE
    STATUS_STOP = xmmsclient.PLAYBACK_STATUS_PAUSE

    def __init__(self, connection):
        EventEmitter.__init__(self)

        self.connection = connection

        self._status = None

        # create events
        self.register(self.STATUS_EVENT)
        self.register(self.VOLUME_EVENT)
        self.register(self.CURRENT_EVENT)

        if connection.connected:
            self._connected()

        connection.listen(connection.CONNECT_EVENT, self._connected)

    def _connected(self):
        xmms = self.connection.xmms

        current_cb = lambda v: self._id_to_info(v, self._current_info)

        # set callbacks
        xmms.broadcast_playback_current_id(current_cb)
        xmms.broadcast_playback_status(self._status_change)
        xmms.broadcast_playback_volume_changed(self._volume_change)

        # get current data
        xmms.playback_current_id(current_cb)
        xmms.playback_status(cb=self._status_change)
        xmms.playback_volume_get(cb=self._volume_change)

    def get_status(self, cb):
        xmms = self.connection.xmms
        xmms.playback_status(lambda v: value_wrap(v, cb))

    def get_current(self, cb):
        xmms = self.connection.xmms
        xmms.playback_current_id(lambda v: self._id_to_info(v, cb))

    def _id_to_info(self, value, cb):
        media_id = value.value()

        if media_id:
            xmms = self.connection.xmms
            xmms.medialib_get_info(media_id, cb=lambda v: value_wrap(v, cb))
        else:
            cb(None)

    def get_status(self, cb):
        xmms = self.connection.xmms
        xmms.playback_status(lambda v: value_wrap(v, cb))

    def _current_info(self, value):
        self.emit(self.CURRENT_EVENT, value)

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

