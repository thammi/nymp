import urwid

# program status
f_status = urwid.SolidFill('S')
status = urwid.BoxAdapter(f_status, 1)

# current media status
f_current = urwid.SolidFill('C')
current = urwid.BoxAdapter(f_status, 3)

# media browser
browser = urwid.SolidFill('B')

# playlist
playlist = urwid.SolidFill('P')

split = urwid.Columns([browser, playlist])

frame = urwid.Frame(split, current, status)

loop = urwid.MainLoop(frame, event_loop=urwid.GLibEventLoop())
loop.run()

