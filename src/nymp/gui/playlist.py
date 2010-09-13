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

from nymp.gui.widgets import SelectableText, ScrollableList
from nymp.gui.update import update

class PlaylistItem:

    def __init__(self, media_id):
        self.media_id = media_id
        self.meta = None
        self.requested = False

    def get(self, key):
        meta = self.meta
        if key in meta:
            return meta[key]
        else:
            return "Unknown"

    def request(self, xc, cb):
        if not self.requested:
            self.requested = True

            xc.playlist.get_info(self.media_id, lambda v: self._info_cb(v, cb))

    def _info_cb(self, meta, cb):
        self.meta = meta
        cb(meta)

class CurPlaylistWalker(urwid.ListWalker):

    PRE_CACHING = 10

    def __init__(self, xc):
        self.xc = xc

        self.playlist = []
        self.selected = []
        self.cur = None
        self.position = None
        self._focus = 0

        playlist = xc.playlist
        playlist.listen(playlist.LOAD_EVENT, self._playlist_loaded)
        playlist.listen(playlist.CHANGE_EVENT, self._playlist_changed)
        playlist.listen(playlist.POSITION_EVENT, self._position_changed)

        if xc.connected:
            self._connect()
        xc.listen(xc.CONNECT_EVENT, self._connect)

    def _connect(self):
        self.xc.playlist.current_playlist(self._playlist_loaded)

    def _playlist_loaded(self, name):
        # save new name
        self.cur = name

        # reset to sane defaults while waiting
        self.playlist = []
        self.position = None
        self._focus = 0

        # request data
        self.xc.playlist.list_entries(name, self._entries_cb)
        self.xc.playlist.position(name, self._position_changed)

    def _playlist_changed(self, event):
        pl = self.xc.playlist

        handler = {
                # TODO: sort, shuffle, update
                pl.CHANGE_ADD: self._change_insert,
                pl.CHANGE_INSERT: self._change_insert,
                pl.CHANGE_CLEAR: self._change_clear,
                pl.CHANGE_REMOVE: self._change_remove,
                pl.CHANGE_MOVE: self._change_move,
                }

        event_type = event['type']
        if event_type in handler:
            handler[event_type](event)
        else:
            raise NotImplementedError

    def _change_move(self, event):
        playlist = self.playlist

        tmp = playlist[event['position']]
        del playlist[event['position']]
        playlist.insert(event['newposition'], tmp)

        self.modified()

    def _change_insert(self, event):
        item = PlaylistItem(event['id'])
        self.playlist.insert(event['position'], item)

        self.modified()

    def _change_remove(self, event):
        position = event['position']
        del self.playlist[position]

        if position < self._focus or len(self.playlist) <= self._focus:
            self._focus -= 1

        self.modified()

    def _change_clear(self, event):
        self._focus = 0
        self.playlist = []
        self.modified()

    def _position_changed(self, position):
        if position['name'] == self.cur:
            self.position = position['position']
            self.modified()

    def _entries_cb(self, data):
        self.playlist = [PlaylistItem(mid) for mid in data]

    def modified(self):
        self._modified()
        update()

    def _get_widget(self, pos):
        playlist = self.playlist
        item = playlist[pos]

        def request_cb(meta):
            self.modified()

        # make sure we get metadata
        item.request(self.xc, request_cb)

        # pre-cache
        for i in range(1, self.PRE_CACHING + 1):
            if pos - i >= 0:
                playlist[pos-i].request(self.xc, request_cb)
            if pos + i < len(playlist):
                playlist[pos+i].request(self.xc, request_cb)

        # what should we display?
        if item.meta:
            content = u"{0} [{2} by {1}]".format(item.get('title'), item.get('artist'), item.get('album'))
        else:
            content = unicode(item.media_id)

        text = SelectableText(content, wrap='clip')

        # are we in the spotlight?
        if pos in self.selected:
            return urwid.AttrMap(text, 'selected', 'selected_focus')
        elif self.position == pos:
            return urwid.AttrMap(text, 'current', 'current_focus')
        else:
            return urwid.AttrMap(text, 'normal', 'focus')

    def get_focus(self):
        if len(self.playlist):
            focus = self._focus
            return (self._get_widget(focus), focus)
        else:
            return (None, None)

    def get_next(self, pos):
        if pos < len(self.playlist) - 1:
            new_pos = pos + 1
            widget = self._get_widget(new_pos)
            return (widget, new_pos)
        else:
            return (None, None)

    def get_prev(self, pos):
        if pos > 0:
            new_pos = pos - 1
            widget = self._get_widget(new_pos)
            return (widget, new_pos)
        else:
            return (None, None)

    def set_focus(self, pos):
        self._focus = pos
        self._modified()

    def goto(self):
        self.xc.playlist.goto(self._focus)

    def delete_entry(self):
        if self.playlist:
            pl = self.xc.playlist
            selected = self.selected

            if selected:
                # remove all selected
                for i in sorted(selected, reverse=True):
                    pl.remove_entry(i, self.cur)

                self.clear_select()
            else:
                # remove item in focus
                pl.remove_entry(self._focus, self.cur)

    def toggle_select(self):
        focus = self._focus
        selected = self.selected

        # toggle focus
        if focus in selected:
            selected.remove(focus)
        else:
            selected.append(focus)

        self._modified()

    def clear_select(self):
        self.selected = []

        self._modified()

    def move(self, delta):
        playlist = self.xc.playlist
        selected = self.selected

        if selected:
            # move selected items

            if delta < 0:
                # top down
                selected.sort()

                # bump?
                if selected[0] + delta < 0:
                    return
            else:
                # bottom up
                selected.sort(reverse=True)

                # bump?
                if selected[0] + delta >= len(self.playlist):
                    return

            # move each item
            for i, pos in enumerate(selected):
                new_pos = pos + delta
                playlist.move_entry(pos, new_pos, self.cur)
                selected[i] = new_pos
        else:
            # move item in focus
            focus = self._focus
            new_focus = focus + delta

            # bump?
            if new_focus < 0 or new_focus >= len(self.playlist):
                return

            # movement
            playlist.move_entry(focus, new_focus, self.cur)
            self._focus = new_focus

    def move_up(self):
        self.move(-1)

    def move_down(self):
        self.move(1)

class Playlist(ScrollableList):

    def __init__(self, xc):
        self.xc = xc

        self.walker = walker = CurPlaylistWalker(xc)
        urwid.ListBox.__init__(self, walker)

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press' and (button == 3 or button == 11):
            actions = {
                    # left button
                    3: self.walker.toggle_select,
                    # double click (right)
                    11: self.walker.goto,
                }

            # select item under the mouse
            offset, inset = self.get_focus_offset_inset(size)
            self.move_focus(size, row - offset)

            actions[button]()
        else:
            ScrollableList.mouse_event(self, size, event, button, col, row, focus)


    def keypress(self, size, key):
        def toggle_walk():
            self.walker.toggle_select()
            self.move_focus(size, 1)

        hotkeys = {
                'd': self.walker.delete_entry,
                ' ': toggle_walk,
                'meta  ': self.walker.clear_select,
                'enter': self.walker.goto,
                'K': self.walker.move_up,
                'J': self.walker.move_down,
            }

        if key in hotkeys:
            hotkeys[key]()
        else:
            return ScrollableList.keypress(self, size, key)

    def move_top(self, size):
        # moving up without iterating
        self.change_focus(size, 0)

    def move_bottom(self, size):
        # moving down without iterating
        self.change_focus(size, len(self.walker.playlist)-1)

