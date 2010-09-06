##############################################################################
##
##  nymp - a graphical xmms2 cli frontend
##  Copyright 2010 Thammi
##
##  pymucl is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  pymucl is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with pymucl.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

import urwid

class ScrollableList(urwid.ListBox):

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press' and (button == 4 or button == 5):
            walker = self.walker
            offset, inset = self.get_focus_offset_inset(size)
            _, cur_pos = walker.get_focus()

            if button == 4:
                _, new_pos = walker.get_prev(cur_pos)
                new_offset = offset - 1 if offset > 0 else offset
            else:
                _, new_pos = walker.get_next(cur_pos)
                new_offset = offset + 1 if offset + 1 < size[1] else offset

            if new_pos != None:
                self.change_focus(size, new_pos, new_offset)

            return None
        else:
            return urwid.ListBox.mouse_event(self, size, event, button, col, row, focus)

class SelectableText(urwid.Text):

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

