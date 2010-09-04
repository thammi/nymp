import urwid

from update import update
from xmms import reduce_meta

class CurrentWidget(urwid.Pile):

    def __init__(self, xc):
        title = self.title = urwid.Text("", 'right')
        album = self.album = urwid.Text("", 'right')
        artist = self.artist = urwid.Text("", 'right')

        urwid.Pile.__init__(self, [title, album, artist])

        player = xc.player

        if xc.connected:
            player.get_current(self._update)

        player.listen(player.CURRENT_EVENT, self._update)

    def _update(self, meta):
        if meta:
            rm = reduce_meta(meta)
            
            self.title.set_text("%i. %s" % (rm['tracknr'], rm['title']))
            self.album.set_text(rm['album'])
            self.artist.set_text(rm['artist'])
        else:
            self.title.set_text("")
            self.album.set_text("")
            self.artist.set_text("")
        
        update()

        # TODO: ugly!
        #from main import loop
        #loop.draw_screen()

