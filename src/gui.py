import urwid
import xmms

class CurrentWidget(urwid.Pile):

    def __init__(self, xc):
        title = self.title = urwid.Text("", 'right')
        album = self.album = urwid.Text("", 'right')
        artist = self.artist = urwid.Text("", 'right')

        urwid.Pile.__init__(self, [title, album, artist])

        player = xc.player
        player.listen(player.CURRENT_EVENT, self._update)

    def _update(self, meta):
        rm = xmms.reduce_meta(meta)
        
        self.title.set_text("%i. %s" % (rm['tracknr'], rm['title']))
        self.album.set_text(rm['album'])
        self.artist.set_text(rm['artist'])

        # TODO: ugly!
        loop.draw_screen()


class BaseWidget(urwid.Frame):

    def __init__(self):
        xc = self.xc = xmms.XmmsConnection()

        # program status
        f_status = urwid.SolidFill('S')
        status = urwid.BoxAdapter(f_status, 1)

        # current media status
        current = CurrentWidget(xc)

        # media browser
        browser = urwid.SolidFill('B')

        # playlist
        playlist = urwid.SolidFill('P')

        split = urwid.Columns([browser, playlist])

        urwid.Frame.__init__(self, split, current, status)

        xc.connect()

    def keypress(self, size, inp):
        if urwid.Frame.keypress(self, size, inp):
            xc = self.xc

            hotkeys = {
                    'p': lambda: xc.player.toggle(),
                    'n': lambda: xc.player.forward(),
                    }

            if inp in hotkeys:
                hotkeys[inp]()


frame = BaseWidget()
loop = urwid.MainLoop(frame, event_loop=urwid.GLibEventLoop())
loop.run()

