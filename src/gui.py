import urwid

# current media status
f_status = urwid.SolidFill('C')
status = urwid.BoxAdapter(f_status, 3)

# media browser
browser = urwid.SolidFill('B')

# playlist
playlist = urwid.SolidFill('P')

split = urwid.Columns([browser, playlist])

frame = urwid.Frame(split, status)

loop = urwid.MainLoop(frame, event_loop=urwid.GLibEventLoop())
loop.run()

