import urwid

from gui import BaseWidget

frame = BaseWidget()
loop = urwid.MainLoop(frame, event_loop=urwid.GLibEventLoop())
loop.run()


