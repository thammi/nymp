_update_fun = None

def update():
    if _update_fun:
        _update_fun()
        return True
    else:
        return False

def register_update(update_fun):
    global _update_fun
    _update_fun = update_fun
