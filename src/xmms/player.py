import xmmsclient

from events import EventEmitter

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

        self._status = self.STATUS_STOP

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
        media_id = value.value()

        if media_id:
            xmms = self.connection.xmms
            xmms.medialib_get_info(value.value(), cb=self._current_info)
        else:
            self.emit(self.STATUS_EVENT, None)

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

