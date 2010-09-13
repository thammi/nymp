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

import os

from xmmsclient import XMMS
from xmmsclient.glib import GLibConnector

from nymp.events import EventEmitter

from nymp.xmms.player import Player
from nymp.xmms.playlist import Playlist

from nymp.xmms.helper import CLIENT_ID

class XmmsConnection(EventEmitter):
    """Represantation of a XMMS connection. Use the modules (player)."""

    CONNECT_EVENT = "connect"
    DISCONNECT_EVENT = "disconnect"

    def __init__(self):
        """Create an unconnected connection represantation"""
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
                xmms = self.xmms = XMMS(CLIENT_ID)

                path = os.environ.get("XMMS_PATH", None)

                xmms.connect(path, disconnect_func=disconnected)
                GLibConnector(xmms)
            except IOError:
                # sad, no connection for you!
                self.xmms = None
                self.connected = False
            else:
                # no exception, we should be connected
                self.connected = True
                self.emit(self.CONNECT_EVENT)

        return self.connected

