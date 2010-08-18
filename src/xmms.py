from xmmsclient import XMMS, userconfdir_get
from xmmsclient.glib import GLibConnector
from os.path import join

# TODO: think of a cool name
_ID = 'INSERT_NAME_HERE'

def get_config_dir():
    return join(userconfdir_get(), "clients", _ID)

class XmmsConnection:

    def __init__(self):
        self.connected = False
        self.xmms = None

        self.connect()

    def connect(self):
        if not self.connected:
            def disconnected(r):
                self.connected = False

            try:
                xmms = self.xmms = XMMS(_ID)

                # TODO: use path conventions
                xmms.connect(disconnect_func=disconnected)
                GLibConnector(xmms)

                xmms.broadcast_playback_status(p)
            except IOError:
                self.xmms = None
                self.connected = False
            else:
                self.connected = True

        return self.connected

