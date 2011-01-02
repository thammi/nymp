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

from nymp.events import EventEmitter

from nymp.xmms.helper import value_wrap

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
        xmms.playback_status(value_wrap(cb))

    def get_current(self, cb):
        xmms = self.connection.xmms
        xmms.playback_current_id(lambda v: self._id_to_info(v, cb))

    def _id_to_info(self, value, cb):
        media_id = value.value()

        if media_id:
            xmms = self.connection.xmms
            xmms.medialib_get_info(media_id, cb=value_wrap(cb))
        else:
            cb(None)

    def _current_info(self, value):
        self.emit(self.CURRENT_EVENT, value)

    def _status_change(self, value):
        status = self._status = value.value()
        self.emit(self.STATUS_EVENT, status)

    def _volume_change(self, value):
        self.emit(self.VOLUME_EVENT, value.value())

    def toggle(self, cb=None):
        if self._status == self.STATUS_PLAY:
            self.pause(cb)
        else:
            self.start(cb)

    def pause(self, cb=None):
        self.connection.xmms.playback_pause(value_wrap(cb))

    def start(self, cb=None):
        self.connection.xmms.playback_start(value_wrap(cb))

    def stop(self, cb=None):
        self.connection.xmms.playback_stop(value_wrap(cb))

    def _go_rel(self, delta, cb=None):
        xmms = self.connection.xmms

        def status_cb(status):
            if status != self.STATUS_PLAY:
                self.start(cb)
            elif cb:
                cb(status)

        def tickle_cb(value):
            self.get_status(status_cb)

        def next_cb(value):
            xmms.playback_tickle(tickle_cb)

        xmms.playlist_set_next_rel(delta, next_cb)

    def next(self, cb=None):
        self._go_rel(1, cb)

    def prev(self, cb=None):
        self._go_rel(-1, cb)

    def set_volume(self, name, volume, cb=None):
        self.connection.xmms.playback_volume_set(name, volume, value_wrap(cb))

    def get_volume(self, cb):
        self.connection.xmms.playback_volume_get(value_wrap(cb))

    def playtime_signal(self, cb):
        self.connection.xmms.signal_playback_playtime(value_wrap(cb))

    def get_playtime(self, cb):
        self.connection.xmms.playback_playtime(value_wrap(cb))

