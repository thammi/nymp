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
import sys
import logging

from nymp.gui.current import CurrentWidget
from nymp.gui.browser import BrowserWidget
from nymp.gui.playlist import Playlist
from nymp.gui.status import StatusBar

from nymp.gui.commands import commands, parse_command

class MiddleColumns(urwid.Columns):

    def keypress(self, size, key):
        # we don't want to change the column with arrow keys
        filtered = ['right', 'left']
        if key not in filtered:
            return urwid.Columns.keypress(self, size, key)
        else:
            return self.get_focus().keypress(size, key)

    def mouse_event(self, size, event, button, col, row, focus):
        # move focus to clicked column
        if event == 'mouse press':
            widths = self.column_widths(size)

            # finding the clicked column
            x = 0
            for column, width in enumerate(widths):
                x += width + self.dividechars

                # we found it
                if col < x:
                    # skip the divider
                    if column % 2 == 0:
                        self.set_focus(column)

                    break

        urwid.Columns.mouse_event(self, size, event, button, col, row, focus)


class BaseWidget(urwid.Frame):

    def __init__(self, xc):
        self.xc = xc
        self.last_click = {}

        # spacer
        hor_space = urwid.AttrMap(urwid.SolidFill(u'\u2502'), 'spacer')
        vert_space = urwid.AttrMap(urwid.Divider(u'\u2500'), 'spacer')

        # program status
        status = urwid.AttrMap(StatusBar(), 'status')

        # current media status
        current = CurrentWidget(xc)
        current_pile = urwid.Pile([current, vert_space])

        # media browser
        browser = BrowserWidget(xc)

        # playlist
        playlist = Playlist(xc)

        widgets = [('weight', 0.6, browser), ('fixed', 1, hor_space), playlist]
        self.split = split = MiddleColumns(widgets, focus_column=2, dividechars=1)

        urwid.Frame.__init__(self, split, current_pile, status)

        self.init_commands()

    def init_commands(self):
        self.hotkeys = hotkeys = {}

        for command, bindings in commands.items():
            for binding in bindings:
                hotkeys[binding] = command

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

        if event == 'mouse press' and  button in DOUBLE_CLICKABLE:
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
            hotkeys = self.hotkeys

            if inp in hotkeys:
                command, args = parse_command(hotkeys[inp])

                if not self.command(size, command, args):
                    logging.info("The command '%s' did not apply" % command)
            else:
                logging.info("No key binding for '%s' found" % inp)

    def command(self, size, command, args):
            xc = self.xc

            # TODO: move somewhere else
            def rel_volume(diff):
                player = xc.player

                def set_volume(cur):
                    new = {}

                    for c in cur:
                        player.set_volume(c, diff + cur[c])

                player.get_volume(set_volume)

            commands = {
                    'play': xc.player.toggle,
                    'next': xc.player.next,
                    'prev': xc.player.prev,
                    'col_swap': self.focus_swap,
                    'col_left': lambda: self.split.set_focus(0),
                    'col_right': lambda: self.split.set_focus(2),
                    'clear': xc.playlist.clear,
                    'quit': sys.exit,
                    'vol_up': lambda: rel_volume(2),
                    'vol_down': lambda: rel_volume(-2),
                    }

            if command in commands:
                commands[command]()
                return True
            else:
                # command
                split = self.split

                # get the focused widget
                focus = split.get_focus()

                if hasattr(focus, 'command'):
                    # calculate width of the widget
                    focus_i = split.get_focus_column()
                    width = split.column_widths(size)[focus_i]

                    # calculate height of the widget
                    (head_height, foot_height), _ = self.frame_top_bottom(size, 'body')
                    height = size[1] - head_height - foot_height

                    return focus.command((width, height), command, args)
                else:
                    return False

