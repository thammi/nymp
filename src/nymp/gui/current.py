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

import urwid
import time

from nymp.xmms import reduce_meta

from nymp.gui.loop import update, deferred_call
from nymp.gui.widgets import TextProgress

def usec_format(usec):
    sec = usec / 1000
    return "%02i:%02i" % (sec / 60, sec % 60)

class CurrentProgress(TextProgress):

    def text(self):
        return "%s / %s" % (usec_format(self.current), usec_format(self.done))

class CurrentWidget(urwid.Columns):

    def __init__(self, xc):
        self.duration = 0

        meta = self.create_meta()
        bar = self.create_progress()

        urwid.Columns.__init__(self, [bar, ('weight', 0.5, meta)])

        xc.listen(xc.CONNECT_EVENT, self._connect)

        player = xc.player

        if xc.connected:
            player.get_current(self._update)
            player.playtime_signal(self._progress)

        player.listen(player.CURRENT_EVENT, self._update)

    def create_meta(self):
        title = self.title = urwid.Text("", 'right')
        album = self.album = urwid.Text("", 'right')
        artist = self.artist = urwid.Text("", 'right')

        widgets = [urwid.AttrMap(text, 'playing') for text in title, album, artist]

        return urwid.Pile(widgets)

    def create_progress(self):
        self.bar = bar = CurrentProgress('pg normal', 'pg complete', done=1, satt='pg smooth')

        col_bar = urwid.Columns([
            ('fixed', 2, urwid.Text(('pg spacer', ' ['))),
            bar,
            ('fixed', 2, urwid.Text(('pg spacer', '] '))),
            ])

        return urwid.Pile([urwid.Text(''), col_bar])

    def _connect(self):
        player.playtime_signal(self._progress)

    def _progress(self, progress):
        self.bar.set_completion(progress)
        update()

    def _update(self, meta):
        if meta:
            rm = reduce_meta(meta)
        else:
            rm = {}
            
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
            elif rm == {}:
                # nothing loaded
                title = ""
            else:
                # tag your library :P
                title = "Unknown"

        album = rm['album'] if 'album' in rm else ""
        artist = rm['artist'] if 'artist' in rm else ""

        self.title.set_text(title)
        self.album.set_text(album)
        self.artist.set_text(artist)

        self.bar.set_done(rm['duration'] if 'duration' in rm else 0)
 
        update()

