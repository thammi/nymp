import urwid

from widgets import SelectableText
from update import update

class PlaylistItem:

    def __init__(self, media_id):
        self.media_id = media_id
        self.meta = None
        self.requested = False

    def request(self, xc):
        raise notimplementederror

    def delete(self, xc):
        raise notimplementederror

    def move_up(self, xc):
        raise notimplementederror

    def move_down(self, xc):
        raise notimplementederror

class CurPlaylistWalker(urwid.ListWalker):

    def __init__(self, xc):
        self.xc = xc

        self.playlist = []
        self.cur = None
        self.position = None

        playlist = xc.playlist
        playlist.listen(playlist.LOAD_EVENT, self._playlist_loaded)
        playlist.listen(playlist.CHANGE_EVENT, self._playlist_changed)
        playlist.listen(playlist.POSITION_EVENT, self._position_changed)

        if xc.connected:
            self._connect()
        xc.listen(xc.CONNECT_EVENT, self._connect)

    def _connect(self):
        pass

    def _playlist_loaded(self, name):
        self.cur = name
        self.xc.playlist.list_entries(name, self._playlist_data_cb)
        self.xc.playlist.position(name, self._position_changed)

    def _playlist_changed(self, event):
        pass

    def _position_changed(self, position):
        self.position = position
        self.modified()

    def _entries_cb(self, data):
        print data
    
    def modified(self):
        self._modified()
        update()

    def get_focus(self):
        return (None, None)
    
    def get_next(self, pos):
        return (None, None)

    def get_pref(self, pos):
        return (None, None)

    def set_focus(self, pos):
        self._focus = pos

class Playlist(urwid.ListBox):

    def __init__(self, xc):
        self.xc = xc

        self.walker = walker = CurPlaylistWalker(xc)
        urwid.ListBox.__init__(self, walker)

