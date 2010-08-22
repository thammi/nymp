import urwid

from gui import BaseWidget

palette = [
        ('focus', 'dark green', 'black'),
        ('normal', 'default', 'black'),
        ]

frame = BaseWidget()
loop = urwid.MainLoop(frame, palette, event_loop=urwid.GLibEventLoop())
loop.run()


