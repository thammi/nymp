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

commands = {
        'global': {
            # navigation
            'nav_up': ['up', 'k'],
            'nav_page_up': ['page up'],
            'nav_down': ['down', 'j'],
            'nav_page_down': ['page down'],
            'nav_top': ['home'],
            'nav_bottom': ['end'],
            'col_swap': ['tab'],
            'col_left': ['h'],
            'col_right': ['l'],
            # playback
            'play': ['x'],
            'stop': ['c'],
            'next': ['v'],
            'prev': ['z'],
            'vol_down': ['9'],
            'vol_up': ['0'],
            'clear': ['C'],
            # global
            'quit': ['q'],
            },
        'playlist': {
            # playlist manipulation
            'yank': ['y'],
            'paste': ['p'],
            'delete': ['d'],
            'mark': [' '],
            'reset_mark': ['meta  '],
            'move_up': ['K'],
            'move_down': ['J'],
            },
        'browser': {
            # browser
            'yank': ['y'],
            'add': ['a'],
            'expand': ['right'],
            'fold': ['left', 'enter'],
            },
        }

def parse_command(cmd_str):
    parts = cmd_str.split()
    return (parts[0], parts[1:])

