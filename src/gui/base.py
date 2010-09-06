import urwid

from current import CurrentWidget
from browser import BrowserWidget
from playlist import Playlist

class MiddleColumns(urwid.Columns):

    def keypress(self, size, key):
        # we don't want to change the column with arrow keys
        filtered = ['right', 'left']
        if key not in filtered:
            return urwid.Columns.keypress(self, size, key)
        else:
            return self.get_focus().keypress(size, key)


class BaseWidget(urwid.Frame):

    def __init__(self, xc):
        self.xc = xc

        # spacer
        hor_space = urwid.AttrMap(urwid.SolidFill(unichr(9474)), 'spacer')

        # program status
        status = urwid.AttrMap(urwid.Text("... i am a status bar ... someday ..."), 'normal')

        # current media status
        current = CurrentWidget(xc)

        # media browser
        browser = BrowserWidget(xc)

        # playlist
        playlist = Playlist(xc)

        widgets = [('weight', 0.6, browser), ('fixed', 1, hor_space), playlist]
        self.split = split = MiddleColumns(widgets, focus_column=2, dividechars=1)

        urwid.Frame.__init__(self, split, current, status)
    
    def focus_swap(self):
        split = self.split
        split.set_focus(0 if split.get_focus_column() else 2)

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

