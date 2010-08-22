import urwid
import xmmsclient.collections as coll

def _node_cmp_key(item):
    """Calculate the key used to sort nodes, ignores case"""
    key = item.data[0]

    if isinstance(key, basestring):
        return key.lower()
    else:
        return key

class CollectionTree:

    def __init__(self, xc, steps, data=None, base=coll.Universe()):
        self.xc = xc
        self.steps = steps
        self.data = data
        self.base = base

        self.requested = False
        self.childs = None
        self.expanded = False

        self.is_leaf = len(self.steps) == 0

    def toggle_exp(self):
        if self.expanded:
            self.fold()
        else:
            self.expand()

    def expand(self):
        if not self.requested:
            self.request()

        self.expanded = True

    def fold(self):
        self.expanded = False

    def request(self, cb=None):
        def acc_cb(value):
            self._coll_cb(value)
            if cb:
                cb()

        xmms = self.xc.xmms
        xmms.coll_query_infos(self.base, self.steps[0], cb=acc_cb)
        self.requested = True

    def _build_child(self, item):
        """Turn a collection item into a node"""
        steps = self.steps

        # turn the dictionary into a list
        data = [item[attr] for attr in steps[0]]

        # create the new collection
        sub_coll = self.base
        for attr in steps[0]:
            value = item[attr]

            if value == None:
                # special case if the property doesn't exist
                sub_coll = coll.Complement(coll.Has(sub_coll, field=attr))
            else:
                # SRSLY? why do I have to care about encoding here????
                if isinstance(value, basestring):
                    value = value.encode("utf-8")
                else:
                    value = unicode(value)
                sub_coll = coll.Equals(sub_coll, field=attr, value=value)

        # actually create the node
        return CollectionTree(self.xc, steps[1:], data, sub_coll)

    def _coll_cb(self, value):
        raw = value.value()

        # turn it into a sorted list
        self.childs = sorted((self._build_child(item) for item in raw),
                key=_node_cmp_key)


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
            icon = "*"
        elif node.expanded and node.childs == None:
            icon = "~"
        elif node.expanded:
            icon = "-"
        else:
            icon = "+"

        text = "%s%s %s" % (spacer, icon, name)
        return urwid.AttrMap(SelectableText(text), 'normal', 'focus')

    def focus_node(self):
        focus = self._focus

        return self._find_node(focus)

    def get_focus(self):
        focus = self._focus

        node = self._find_node(focus)

        if node:
            widget = self._build_widget(node, focus)
            return (widget, focus)
        else:
            return (None, None)

    def get_next(self, pos, force_forward=False):
        # get current node
        cur = self._find_node(pos)

        # where to go?
        if cur.expanded and cur.childs and not force_forward:
            pos = list(pos) + [0]
        else:
            pos = list(pos)
            pos[-1] += 1

        node = self._find_node(pos)

        if node:
            widget = self._build_widget(node, pos)
            return (widget, pos)
        else:
            if len(pos) > 1:
                return self.get_next(pos[:-1], True)
            else:
                return (None, None)

    def get_prev(self, pos):
        pos = list(pos)
        pos[-1] -= 1

        if pos[-1] < 0:
            if len(pos) > 1:
                pos = pos[:-1]
                node = self._find_node(pos)
                widget = self._build_widget(node, pos)
                return (widget, pos)
            else:
                return (None, None)
        else:
            while True:
                node = self._find_node(pos)

                if not node.expanded or not node.childs:
                    widget = self._build_widget(node, pos)
                    return (widget, pos)
                else:
                    pos += [len(node.childs)-1]

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

        steps = [['artist'], ['date', 'album'], ['tracknr', 'title']]
        self.coll_tree = coll_tree = CollectionTree(xc, steps)
        self.walker = walker = CollTreeWalker(coll_tree)

        urwid.ListBox.__init__(self, walker)

    def _connect(self):
        self.coll_tree.request(self.walker.update)

    def keypress(self, size, key):
        if key == 'enter':
            self.walker.focus_node().toggle_exp()
        elif key == 'right':
            self.walker.focus_node().expand()
        elif key == 'left':
            self.walker.focus_node().fold()
        else:
            urwid.ListBox.keypress(self, size, key)

