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
import xmmsclient.collections as coll

from update import update
from events import EventEmitter
from widgets import SelectableText, ScrollableList

def _node_cmp_key(item):
    """Calculate the key used to sort nodes, ignores case"""
    key = item.data[0]

    if isinstance(key, basestring):
        return key.lower()
    else:
        return key

def _create_collection(data, attributes, base):
    # create the new collection
    new_coll = base

    for value, attr in zip(data, attributes):
        if value == None:
            # special case if the property doesn't exist
            new_coll = coll.Complement(coll.Has(new_coll, field=attr))
        else:
            # SRSLY? why do I have to care about encoding here????
            if isinstance(value, basestring):
                value = value.encode("utf-8")
            else:
                value = unicode(value)

            new_coll = coll.Equals(new_coll, field=attr, value=value)

    return new_coll

class CollectionTree(EventEmitter):

    MODIFY_EVENT = "tree_modified"

    def __init__(self, xc, steps, data=None, parent=None):
        EventEmitter.__init__(self)

        self.xc = xc
        self.steps = steps
        self.data = data
        self.parent = parent

        self.register(self.MODIFY_EVENT)

        if parent:
            self.collection = _create_collection(data, parent.steps[0]['sort'],
                    parent.collection)
        else:
            self.collection = coll.Universe()

        self.requested = False
        self.childs = None
        self.expanded = False

        self.is_leaf = len(self.steps) == 0

    def add_to_playlist(self):
        # flatten the steps
        order = sum((step['sort'] for step in self.steps), [])

        self.xc.playlist.add_collection(self.collection, order)

    def toggle_exp(self):
        if self.expanded:
            self.fold()
        else:
            self.expand()

    def expand(self):
        if not self.requested:
            self.request()

        self.expanded = True

        self._modified()

    def fold(self):
        self.expanded = False

        self._modified()

    def request(self, cb=None):
        if not self.is_leaf:
            def acc_cb(value):
                self._coll_cb(value)
                if cb:
                    cb()

            # TODO: build a wrapper
            xmms = self.xc.xmms
            xmms.coll_query_infos(self.collection, self.steps[0]['sort'], cb=acc_cb)
            self.requested = True

    def _build_child(self, item):
        """Turn a collection item into a node"""
        steps = self.steps

        # turn the dictionary into a list
        data = [unicode(item[attr]) for attr in steps[0]['sort']]

        # actually create the node
        return CollectionTree(self.xc, steps[1:], data, self)

    def _coll_cb(self, value):
        raw = value.value()

        # turn it into a sorted list
        self.childs = sorted((self._build_child(item) for item in raw),
                key=_node_cmp_key)

        self._modified()

    def _modified(self, tree=None):
        if self.parent:
            self.parent._modified()

        if tree == None:
            tree = self

        self.emit(self.MODIFY_EVENT, tree)

    def _format_child(self, data):
        cur_step = self.steps[0]

        if 'format' in cur_step:
            return cur_step['format'].format(*data)
        else:
            return ' - '.join(data)

    def format(self):
        # parents know best ...
        return self.parent._format_child(self.data)


class CollTreeWalker(urwid.ListWalker):

    def __init__(self, tree):
        self.tree = tree
        self._focus = [0]

        #tree.listen(tree.MODIFY_EVENT, lambda t: self._modified())
        tree.listen(tree.MODIFY_EVENT, lambda t: self.update())

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
        spacer = " " * ((len(pos) - 1) * 2)

        if node.is_leaf:
            icon = ""
        elif node.expanded and node.childs == None:
            icon = "~ "
        elif node.expanded:
            icon = "- "
        else:
            icon = "+ "

        text = ''.join((spacer, icon, node.format()))
        # TODO: caching
        return urwid.AttrMap(SelectableText(text, wrap='clip'), 'normal', 'focus')

    def focus_node(self):
        focus = self._focus

        return self._find_node(focus)

    def focus_pos(self):
        return self._focus

    def get_focus(self):
        # TODO: remove when new root is finished
        if self.tree.childs == None:
            return (urwid.Text("Loading ..."), None)

        focus = self._focus

        node = self._find_node(focus)

        if node:
            widget = self._build_widget(node, focus)
            return (widget, focus)
        else:
            return (None, None)

    def get_next(self, pos, force_forward=False):
        # TODO: remove when new root is finished
        if pos == None:
                return (None, None)

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
        # TODO: remove when new root is finished
        if pos == None:
                return (None, None)

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
        update()

class BrowserWidget(ScrollableList):

    def __init__(self, xc):
        self.xc = xc

        steps = [
                # 1: artist
                {
                    'sort': ['artist'],
                },
                # 2: album
                {
                    'sort': ['date', 'album'],
                    'format': u'{0:>4} - {1}',
                },
                # 3: title
                {
                    'sort': ['partofset', 'tracknr', 'title', 'id'],
                    'format': u'{1:>2}. {2}',
                },
            ]

        self.coll_tree = coll_tree = CollectionTree(xc, steps)
        self.walker = walker = CollTreeWalker(coll_tree)

        urwid.ListBox.__init__(self, walker)

        if xc.connected:
            self._connect()
        xc.listen(xc.CONNECT_EVENT, self._connect)

    def _connect(self):
        # TODO: doesn't work with reconnects
        self.coll_tree.request()

    def keypress(self, size, key):
        def deep_fold():
            walker = self.walker
            node = walker.focus_node()

            if node.expanded:
                # we should fold the current node
                node.fold()
            else:
                # let's visit the parent
                pos = walker.focus_pos()

                if len(pos) > 1:
                    walker.set_focus(pos[:-1])
                else:
                    # TODO: tell the user?
                    pass

        hotkeys = {
                'enter': self.walker.focus_node().toggle_exp,
                'right': self.walker.focus_node().expand,
                'left': deep_fold,
                'a': self.walker.focus_node().add_to_playlist,
            }

        if key in hotkeys:
            if self.walker.focus_node():
                hotkeys[key]()
        else:
            return urwid.ListBox.keypress(self, size, key)

