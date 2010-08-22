import urwid

from xmms import XmmsConnection

from current import CurrentWidget
from browser import BrowserWidget
from playlist import Playlist

class BaseWidget(urwid.Frame):

    def __init__(self):
        xc = self.xc = XmmsConnection()

        # program status
        f_status = urwid.SolidFill('S')
        status = urwid.BoxAdapter(f_status, 1)

        # current media status
        current = CurrentWidget(xc)

        # media browser
        browser = BrowserWidget(xc)

        # playlist
        playlist = Playlist(xc)

        self.split = split = urwid.Columns([browser, playlist], focus_column=0)

        urwid.Frame.__init__(self, split, current, status)

        xc.connect()
    
    def focus_swap(self):
        split = self.split
        split.set_focus(0 if split.get_focus_column() else 1)

    def keypress(self, size, inp):
        if urwid.Frame.keypress(self, size, inp):
            xc = self.xc

            hotkeys = {
                    'p': lambda: xc.player.toggle(),
                    'n': lambda: xc.player.forward(),
                    'tab': self.focus_swap,
                    }

            if inp in hotkeys:
                hotkeys[inp]()
            else:
                return inp

