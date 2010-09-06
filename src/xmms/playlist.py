from events import EventEmitter
from helper import value_wrap

# TODO: finish
class Playlist(EventEmitter):
    """Everything considering the playlist"""

    CHANGE_EVENT = "playlist_changed"
    LOAD_EVENT = "playlist_loaded"
    POSITION_EVENT = "position_changed"

    def __init__(self, connection):
        EventEmitter.__init__(self)
        
        self.register(self.CHANGE_EVENT)
        self.register(self.LOAD_EVENT)
        self.register(self.POSITION_EVENT)

        self.connection = connection

        self.current = None

        connection.listen(connection.CONNECT_EVENT, self._connected)

    def add_collection(self, coll, order, playlist=None, cb=None):
        xmms = self.connection.xmms
        xmms.playlist_add_collection(coll, order, playlist, value_wrap(cb))

    def clear(self, playlist=None, cb=None):
        xmms = self.connection.xmms
        xmms.playlist_clear(coll, order, playlist, value_wrap(cb))

    def current_playlist(self, cb):
        xmms = self.connection.xmms
        xmms.playlist_current_active(value_wrap(cb))

    def position(self, playlist, cb):
        xmms = self.connection.xmms
        xmms.playlist_current_pos(playlist, value_wrap(cb))

    def list_entries(self, playlist, cb):
        xmms = self.connection.xmms
        xmms.playlist_list_entries(playlist, value_wrap(cb))

    def list_playlists(self, cb):
        xmms = self.connection.xmms
        xmms.playlist_list(value_wrap(cb))

    def move_entry(self, old, new, playlist=None, cb=None):
        xmms = self.connection.xmms
        xmms.playlist_move(old, new, playlist, value_wrap(cb))

    def move_entry(self, media_id, playlist=None, cb=None):
        xmms = self.connection.xmms
        xmms.playlist_remove_entry(old, new, playlist, value_wrap(cb))

    def get_info(self, media_id, cb):
        xmms = self.connection.xmms
        xmms.medialib_get_info(media_id, value_wrap(cb))

    def _connected(self):
        xmms = self.connection.xmms

        # set callbacks
        xmms.broadcast_playlist_changed(self._change)
        xmms.broadcast_playlist_loaded(self._loaded)
        xmms.broadcast_playlist_current_pos(self._position)

    def _position(self, value):
        self.emit(self.POSITION_EVENT, value.value())

    def _change(self, value):
        self.emit(self.CHANGE_EVENT, value.value())

    def _loaded(self, value):
        self.emit(self.LOAD_EVENT, value.value())

