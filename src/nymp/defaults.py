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

defaults = {
        'hotkeys': {
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
                'activate': ['enter'],
                },
            'browser': {
                # browser
                'yank': ['y'],
                'add': ['a'],
                'expand': ['right'],
                'fold': ['left', 'enter'],
                },
            },

        'palettes': {
            'normal': {
                'normal': ('default', 'default'),
                'focus': ('black', 'light gray'),
                'current': ('dark green', 'default'),
                'current_focus': ('default', 'dark gray'),
                'spacer': ('dark gray', 'default'),
                'status': ('dark gray', 'default'),
                'playing': ('dark green', 'default'),
                'selected': ('yellow', 'default'),
                'selected_focus': ('yellow', 'dark gray'),
                'progress': ('default', 'dark gray'),
                },
            'high': {
                'normal': ('#FFF', '#000'),
                'focus': ('#000', '#666'),
                'current': ('#393', '#000'),
                'current_focus': ('#FFF', '#666'),
                'spacer': ('#666', '#000'),
                'status': ('#666', '#000'),
                'playing': ('#393', '#000'),
                'selected': ('#FF0', '#000'),
                'selected_focus': ('#FF0', '#666'),
                'progress': ('#000', '#999'),
                },
            'mono': {
                'focus': 'standout',
                'current': 'bold,underline',
                'current_focus': 'bold,standout',
                'selected': 'bold',
                'selected_focus': 'bold,standout',
                }
            },
        }

