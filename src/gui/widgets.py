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

class ScrollableList(urwid.ListBox):
    '''A ListBox with mouse scrolling and smoother scrolling with offset'''

    SCROLL_SPACE = 2

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press' and (button == 4 or button == 5):
            if button == 4:
                self.move_focus(size, -1)
            else:
                self.move_focus(size, 1)
        else:
            return urwid.ListBox.mouse_event(self, size, event, button, col, row, focus)

    def keypress(self, size, key):
        hotkeys = {
                'down': lambda: self.move_focus(size, 1),
                'up': lambda: self.move_focus(size, -1),
                'page down': lambda: self.move_focus(size, size[1] - self.SCROLL_SPACE),
                'page up': lambda: self.move_focus(size, -(size[1] - self.SCROLL_SPACE)),
                'home': lambda: self.move_top(size),
                'end': lambda: self.move_bottom(size),
            }

        if key in hotkeys:
            hotkeys[key]()
        else:
            return urwid.ListBox.keypress(self, size, key)

    def move_top(self, size):
        walker = self.walker
        _, cur_pos = walker.get_focus()

        # keep walking
        while True:
            _, new_pos = walker.get_prev(cur_pos)

            # 'till the end
            if new_pos != None:
                cur_pos = new_pos
            else:
                break

        self.change_focus(size, cur_pos)

    def move_bottom(self, size):
        walker = self.walker
        _, cur_pos = walker.get_focus()

        # keep walking
        while True:
            _, new_pos = walker.get_next(cur_pos)

            # 'till the end
            if new_pos != None:
                cur_pos = new_pos
            else:
                break

        self.change_focus(size, cur_pos)

    def move_focus(self, size, delta):
        walker = self.walker
        offset, inset = self.get_focus_offset_inset(size)

        # starting point
        _, cur_pos = walker.get_focus()

        # stepping the desired amount of steps
        for i in xrange(abs(delta)):
            # up or down
            if delta > 0:
                _, new_pos = walker.get_next(cur_pos)
            else:
                _, new_pos = walker.get_prev(cur_pos)

            # stopping at the end
            if new_pos != None:
                cur_pos = new_pos
            else:
                break

        # calculating the new position (display)
        new_offset = offset + delta
        new_offset = min(new_offset, size[1] - 1 - self.SCROLL_SPACE)
        new_offset = max(new_offset, self.SCROLL_SPACE)

        # actually setting the new focus
        self.change_focus(size, cur_pos, new_offset)

class SelectableText(urwid.Text):

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

