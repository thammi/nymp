import urwid

from widgets import SelectableText

class Playlist(urwid.ListBox):

    def __init__(self, xc):
        self.xc = xc

        txt = ["hello", "world"]
        widgets = [urwid.AttrMap(SelectableText(i), 'normal', 'focus') for i in txt]
        urwid.ListBox.__init__(self, widgets)
