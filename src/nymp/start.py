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

from nymp.gui import BaseWidget, get_updater
from nymp.xmms import XmmsConnection

# TODO: remove logging :D
import logging
h = logging.FileHandler('/tmp/log')
rl = logging.getLogger()
rl.addHandler(h)
rl.setLevel(logging.DEBUG)

normal_palette = {
        'normal': ('default', 'default'),
        'focus': ('black', 'light gray'),
        'current': ('dark green', 'default'),
        'current_focus': ('default', 'dark gray'),
        'spacer': ('dark gray', 'default'),
        'status': ('dark gray', 'default'),
        'playing': ('dark green', 'default'),
        'selected': ('yellow', 'default'),
        'selected_focus': ('yellow', 'dark gray'),
        }

high_palette = {
        'normal': ('#FFF', '#000'),
        'focus': ('#000', '#666'),
        'current': ('#393', '#000'),
        'current_focus': ('#FFF', '#666'),
        'spacer': ('#666', '#000'),
        'status': ('#666', '#000'),
        'playing': ('#393', '#000'),
        'selected': ('#FF0', '#000'),
        'selected_focus': ('#FF0', '#666'),
        }

mono_palette = {
        'focus': 'standout',
        'current': 'bold,underline',
        'current_focus': 'bold,standout',
        'selected': 'bold',
        'selected_focus': 'bold,standout',
        }

# merging palettes into the format urwid wants
def palette_mixer(normal, mono, high):
    keys = set()
    for palette in normal, mono, high:
        keys.update(palette.keys())

    for key in keys:
        entry = [key]

        if key in normal:
            normal_entry = normal[key]
        else:
            normal_entry = ['default', 'default']
        entry.extend(normal_entry)

        if key in mono:
            entry.append(mono[key])
        else:
            entry.append('')

        if key in high:
            entry.extend(high[key])
        else:
            entry.extend(normal_entry)

        yield tuple(entry)

def main(args):
    xc = XmmsConnection()
    xc.connect()

    frame = BaseWidget(xc)

    palette = palette_mixer(normal_palette, mono_palette, high_palette)
    loop = urwid.MainLoop(frame, palette, event_loop=urwid.GLibEventLoop())

    #loop.screen.set_terminal_properties(1)
    loop.screen.set_terminal_properties(256)

    get_updater().loop = loop

    loop.run()
