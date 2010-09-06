import urwid

from widgets import SelectableText, ScrollableList
from update import update

class PlaylistItem:

    def __init__(self, media_id):
        self.media_id = media_id
        self.meta = None
        self.requested = False

    def get(self, key):
        meta = self.meta
        if key in meta:
            return meta[key]
        else:
            return "Unknown"

    def request(self, xc, cb):
        if not self.requested:
            self.requested = True

            xc.playlist.get_info(self.media_id, lambda v: self._info_cb(v, cb))

    def _info_cb(self, meta, cb):
        self.meta = meta
        cb(meta)

    def delete(self, xc):
        raise NotImplementedError

    def move_up(self, xc):
        raise NotImplementedError

    def move_down(self, xc):
        raise NotImplementedError

class CurPlaylistWalker(urwid.ListWalker):

    PRE_CACHING = 10

    def __init__(self, xc):
        self.xc = xc

        self.playlist = []
        self.cur = None
        self.position = None
        self._focus = 0

        playlist = xc.playlist
        playlist.listen(playlist.LOAD_EVENT, self._playlist_loaded)
        playlist.listen(playlist.CHANGE_EVENT, self._playlist_changed)
        playlist.listen(playlist.POSITION_EVENT, self._position_changed)

        if xc.connected:
            self._connect()
        xc.listen(xc.CONNECT_EVENT, self._connect)

    def _connect(self):
        self.xc.playlist.current_playlist(self._playlist_loaded)

    def _playlist_loaded(self, name):
        # save new name
        self.cur = name

        # reset to sane defaults while waiting
        self.playlist = []
        self.position = None
        self._focus = 0

        # request data
        self.xc.playlist.list_entries(name, self._entries_cb)
        self.xc.playlist.position(name, self._position_changed)

    def _playlist_changed(self, event):
        # TODO: implement!
        # watch out for focus and position when 
        pass

    def _position_changed(self, position):
        if position['name'] == self.cur:
            self.position = position['position']
            self.modified()

    def _entries_cb(self, data):
        self.playlist = [PlaylistItem(mid) for mid in data]
    
    def modified(self):
        self._modified()
        update()
    
    def _get_widget(self, pos):
        playlist = self.playlist
        item = playlist[pos]

        def request_cb(meta):
            self.modified()

        # make sure we get metadata
        item.request(self.xc, request_cb)

        # pre-cache
        for i in range(1, self.PRE_CACHING + 1):
            if pos - i >= 0:
                playlist[pos-i].request(self.xc, request_cb)
            if pos + i < len(playlist):
                playlist[pos+i].request(self.xc, request_cb)

        # what should we display?
        if item.meta:
            content = u"{0} [{2} by {1}]".format(item.get('title'), item.get('artist'), item.get('album'))
        else:
            content = unicode(item.media_id)

        text = SelectableText(content, wrap='clip')
        
        # are we in the spotlight?
        if self.position == pos:
            return urwid.AttrMap(text, 'current', 'current_focus')
        else:
            return urwid.AttrMap(text, 'normal', 'focus')

    def get_focus(self):
        if len(self.playlist):
            focus = self._focus
            return (self._get_widget(focus), focus)
        else:
            return (None, None)
    
    def get_next(self, pos):
        if pos < len(self.playlist) - 1:
            new_pos = pos + 1
            widget = self._get_widget(new_pos)
            return (widget, new_pos)
        else:
            return (None, None)

    def get_prev(self, pos):
        if pos > 0:
            new_pos = pos - 1
            widget = self._get_widget(new_pos)
            return (widget, new_pos)
        else:
            return (None, None)

    def set_focus(self, pos):
        self._focus = pos
        self._modified()

class Playlist(ScrollableList):

    def __init__(self, xc):
        self.xc = xc

        self.walker = walker = CurPlaylistWalker(xc)
        urwid.ListBox.__init__(self, walker)

