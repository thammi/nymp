import urwid

from gui import BaseWidget
from xmms import XmmsConnection

palette = [
        ('focus', 'dark green', 'default'),
        ('normal', 'default', 'default'),
        ]

xc = XmmsConnection()
xc.connect()

frame = BaseWidget(xc)
loop = urwid.MainLoop(frame, palette, event_loop=urwid.GLibEventLoop())
loop.run()


