# nymp

## About

nymp is a graphical command line client for xmms2. It is library focused and
provides a tree view on your collection.

## Status

The project is already usable but there is still some missing functionality. The
author uses it on a daily basis. See the 'TODO' file for a (probably incomplete
and outdatet) list of planned additional features.

## Dependencies

* XMMS2
* Python 2.X (developed with Python 2.6, tested on Python 2.5)
* urwid (python-urwid in Debian)
* Python bindings for XMMS2 (python-xmmsclient in Debian)

## Usage

### XMMS2

nymp is a frontend for XMMS2. It doesn't play any files by itself but forwards
these tasks to XMMS2. The library is handled by XMMS2 as well.

XMMS2 follows a philosophy related to the Unix principle 'Make each program do
one thing well.'. It offers a client/server infrastructure where multiple
clients are able to manipulate the state of the music playback. You therefore
should use other clients to achieve the best user experience.

The most important task nymp doesn't handle is media library management. You
should install `xmms2-mlib-updater` to automatically import your media files
into the media library and scan for changes. It is part of most distributions.

### Startup

Use `launch.py` in `./src/` to start the program. You can also add a link to it in
your `bin` directory. If nymp is not able to connect to the XMMS2 server,
`xmms2-launcher` is called to start one.

### Key Bindings

The key bindings are subject to change in the near future. They are loosely
vim-oriented. Configuration and a command line will be implemented later.

Incomplete overview:

* x - play/pause
* c - stop
* z/v - previous/next
* d - delete from playlist (and put into buffer)
* a - append to playlist
* p - paste from buffer
* y - save to buffer
* j/k/arrow keys - navigate
* h/l/tab - change column (library/playlist)
* enter - collapse tree node/jump to playlist item
* space - mark/unmark item
* alt+space - unmark all
* 9/0 - change volume

You can use the mouse, too.

## Todo and ideas

- second xmms connection for heavy operations (library ...)
- playlist update (sort, shuffle, update)
- library update
- library browser root?
  - collections
    - collection management?
  - search?
- search
  - find and/or filter?
- adding a command line?
  - hotkeys -> commands?
  - auto completion
- playlists
- playback status

