import urwid

from update import update
from xmms import reduce_meta

class CurrentWidget(urwid.Pile):

    def __init__(self, xc):
        title = self.title = urwid.Text("", 'right')
        album = self.album = urwid.Text("", 'right')
        artist = self.artist = urwid.Text("", 'right')

        widgets = [urwid.AttrMap(text, 'normal') for text in title, album, artist]
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

