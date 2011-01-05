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

Use `launch.py` in `./src/` to start the program. You can also add a link to it in
your `bin` directory.

The key bindings are subject to change in the near future. They are loosely
vim-oriented. Configuration and a command line will be implemented later.

Incomplete overview:

* p - play/pause
* d - delete from playlist
* j/k - navigate
* h/l/tab - change column (library/playlist)
* a - append to playlist
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

