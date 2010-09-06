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

import xmmsclient

from events import EventEmitter
from helper import value_wrap

# TODO: finish
class Playlist(EventEmitter):
    """Everything considering the playlist"""

    CHANGE_EVENT = "playlist_changed"
    LOAD_EVENT = "playlist_loaded"
    POSITION_EVENT = "position_changed"

    CHANGE_CLEAR = xmmsclient.PLAYLIST_CHANGED_CLEAR
    CHANGE_ADD = xmmsclient.PLAYLIST_CHANGED_ADD
    CHANGE_INSERT = xmmsclient.PLAYLIST_CHANGED_INSERT
    CHANGE_MOVE = xmmsclient.PLAYLIST_CHANGED_MOVE
    CHANGE_REMOVE = xmmsclient.PLAYLIST_CHANGED_REMOVE
    CHANGE_SHUFFLE = xmmsclient.PLAYLIST_CHANGED_SHUFFLE
    CHANGE_SORT = xmmsclient.PLAYLIST_CHANGED_SORT
    CHANGE_UPDATE = xmmsclient.PLAYLIST_CHANGED_UPDATE

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

    def remove_entry(self, position, playlist=None, cb=None):
        xmms = self.connection.xmms
        xmms.playlist_remove_entry(position, playlist, value_wrap(cb))

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

