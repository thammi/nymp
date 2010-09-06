##############################################################################
##
##  nymp - a graphical xmms2 cli frontend
##  Copyright 2010 Thammi
##
##  pymucl is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  pymucl is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with pymucl.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

import urwid

from update import update
from xmms import reduce_meta

class CurrentWidget(urwid.Pile):

    def __init__(self, xc):
        title = self.title = urwid.Text("", 'right')
        album = self.album = urwid.Text("", 'right')
        artist = self.artist = urwid.Text("", 'right')

        divider = urwid.AttrMap(urwid.Divider(unichr(9472)), 'spacer')

        widgets = [urwid.AttrMap(text, 'normal') for text in title, album, artist]
        widgets.append(divider)

        urwid.Pile.__init__(self, widgets)

        player = xc.player

        if xc.connected:
            player.get_current(self._update)

        player.listen(player.CURRENT_EVENT, self._update)

    def _update(self, meta):
        if meta:
            rm = reduce_meta(meta)
        else:
            rm = []
            
        if 'title' in rm:
            title = "%i. %s" % (rm['tracknr'], rm['title']) if 'tracknr' in rm else rm['title']
        else:
            title = rm['url'] if 'url' in rm else ""

        album = rm['album'] if 'album' in rm else ""
        artist = rm['artist'] if 'artist' in rm else ""

        self.title.set_text(title)
        self.album.set_text(album)
        self.artist.set_text(artist)
        
        update()

        # TODO: ugly!
        #from main import loop
        #loop.draw_screen()

