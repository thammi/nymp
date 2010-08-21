import urwid

class BrowserWidget(urwid.ListBox):

    def __init__(self, xc):
        self.xc = xc

        l = [urwid.Text('+ item %i'%i) for i in range(256)]

        for t in l:
            t.keypress = lambda s, k: k
            t._selectable = True

        self.walker = walker = urwid.SimpleListWalker(l)

        urwid.ListBox.__init__(self, walker)

