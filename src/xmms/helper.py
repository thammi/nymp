from xmmsclient import userconfdir_get

def get_config_dir():
    """Get configuration directory according to XMMS2 guideline"""
    return join(userconfdir_get(), "clients", _ID)

def reduce_meta(meta):
    tuples = ((name, value) for (plugin, name), value in meta.items())
    return dict(tuples)

def value_wrap(cb):
    if cb:
        return lambda value: cb(value.value())
    else:
        return None

