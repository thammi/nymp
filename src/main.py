import urwid

from gui import BaseWidget

palette = [
        ('focus', 'dark green', 'default'),
        ('normal', 'default', 'default'),
        ]

frame = BaseWidget()
loop = urwid.MainLoop(frame, palette, event_loop=urwid.GLibEventLoop())
loop.run()


