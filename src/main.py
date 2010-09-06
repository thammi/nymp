import urwid

from gui import BaseWidget, get_updater
from xmms import XmmsConnection

normal_palette = {
        'normal': ('default', 'default'),
        'focus': ('black', 'light gray'),
        'current': ('dark green', 'default'),
        'current_focus': ('dark green', 'light gray'),
        'spacer': ('dark gray', 'default'),
        }

high_palette = {
        'normal': ('#FFF', '#000'),
        'focus': ('#0C0', '#666'),
        'current': ('#66F', '#000'),
        'current_focus': ('#00F', '#666'),
        'spacer': ('#666', '#000'),
        }

mono_palette = {
        'focus': 'standout',
        'current': 'underline',
        'current_focus': 'standout',
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

xc = XmmsConnection()
xc.connect()

frame = BaseWidget(xc)

palette = palette_mixer(normal_palette, mono_palette, high_palette)
loop = urwid.MainLoop(frame, palette, event_loop=urwid.GLibEventLoop())

loop.screen.set_terminal_properties(256)

get_updater().loop = loop

loop.run()


