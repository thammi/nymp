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

        divider = urwid.AttrMap(urwid.Divider(u'\u2500'), 'spacer')

        widgets = [urwid.AttrMap(text, 'playing') for text in title, album, artist]
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
            if 'tracknr' in rm:
                # use title and track number
                title = "%i. %s" % (rm['tracknr'], rm['title']) 
            else:
                # use the title only
                title = rm['title']
        else:
            if 'url' in rm:
                # fall back to the url
                url = rm['url']
                title = url[url.rfind('/')+1:]
            else:
                # tag your library :P
                title = "Unknown"

        album = rm['album'] if 'album' in rm else ""
        artist = rm['artist'] if 'artist' in rm else ""

        self.title.set_text(title)
        self.album.set_text(album)
        self.artist.set_text(artist)
        
        update()

        # TODO: ugly!
        #from main import loop
        #loop.draw_screen()

