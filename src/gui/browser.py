import urwid

from xmms import CollectionTree

class SelectableText(urwid.Text):

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

class CollTreeWalker(urwid.ListWalker):

    def __init__(self, tree):
        self.tree = tree
        self._focus = [0]

    def _find_node(self, pos, cur=None):
        if cur == None:
            cur = self.tree

        if cur.childs == None or len(cur.childs) <= pos[0]:
            return None
        else:
            found = cur.childs[pos[0]]
            if len(pos) == 1:
                return found
            else:
                return self._find_node(pos[1:], found)

    def _build_widget(self, node, pos):
        name = u" - ".join((unicode(item) for item in node.data))

        spacer = " " * (len(pos) - 1)

        if node.is_leaf:
            icon = ""
        else:
            icon = "+"

        text = "%s%s %s" % (spacer, icon, name)
        return urwid.AttrMap(SelectableText(text), 'normal', 'focus')

    def get_focus(self):
        focus = self._focus

        node = self._find_node(focus)

        if node:
            widget = self._build_widget(node, focus)
            return (widget, focus)
        else:
            return (None, None)

    def get_next(self, pos):
        pos = list(pos)
        pos[-1] += 1

        node = self._find_node(pos)

        if node:
            widget = self._build_widget(node, pos)
            return (widget, pos)
        else:
            if len(pos) > 1:
                return self.get_next(pos[:-1])
            else:
                return (None, None)

    def get_prev(self, pos):
        pos = list(pos)
        pos[-1] -= 1

        if pos[-1] < 0:
            if len(pos) > 1:
                return self.get_prev(pos[:-1])
            else:
                return (None, None)
        else:
            node = self._find_node(pos)
            widget = self._build_widget(node, pos)
            return (widget, pos)

    def set_focus(self, pos):
        self._focus = pos
        self._modified()

    def update(self):
        self._modified()

class BrowserWidget(urwid.ListBox):

    def __init__(self, xc):
        self.xc = xc

        xc.listen(xc.CONNECT_EVENT, self._connect)

        l = [urwid.AttrMap(SelectableText('+ item %i'%i), 'normal', 'focus')
                for i in range(256)]

        steps = [['artist'], ['year', 'album'], ['tracknr', 'title']]
        self.coll_tree = coll_tree = CollectionTree(xc, steps)
        self.walker = walker = CollTreeWalker(coll_tree)

        urwid.ListBox.__init__(self, walker)

    def _connect(self):
        self.coll_tree.request(self.walker.update)

