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
import time

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
        self.last_click = {}

        # spacer
        hor_space = urwid.AttrMap(urwid.SolidFill(u'\u2502'), 'spacer')

        # program status
        status = urwid.AttrMap(urwid.Text("... i am a status bar ... someday ..."), 'status')

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

    # transparently inserting double click buttons
    # TODO: find a better way to hook this in ... monkey patching?
    # TODO: 'dragging' around fires accidental double-clicks
    def mouse_event(self, size, event, button, col, row, focus):
        # time between the two clicks activating a double click
        DOUBLE_CLICK_TIME = 0.25
        DRAG_PROTECT_TIME = 0.1
        # mouse buttons which can trigger a double click
        DOUBLE_CLICKABLE = [1]

        if button in DOUBLE_CLICKABLE:
            last = self.last_click
            now = time.time()

            if button in last:
                delta = now - last[button]

                # check for double click
                if delta > DRAG_PROTECT_TIME and delta < DOUBLE_CLICK_TIME:
                    # add the magic offset
                    button += 10

            # save current click
            last[button] = now

        urwid.Frame.mouse_event(self, size, event, button, col, row, focus)

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

