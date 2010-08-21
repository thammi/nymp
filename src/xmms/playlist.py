from events import EventEmitter

# TODO: finish
class Playlist(EventEmitter):
    """Everything considering the playlist"""

    CHANGE_EVENT = "playlist_changed"

    def __init__(self, connection):
        EventEmitter.__init__(self)

        self.connection = connection

        self.register(self.CHANGE_EVENT)

        connection.listen(connection.CONNECT_EVENT, self._connected)

    def _connected(self):
        xmms = self.connection.xmms

        # set callbacks
        xmms.broadcast_playlist_changed(self._change)

    def _change(self, value):
        self.emit(self.CHANGE_EVENT, value.value())

