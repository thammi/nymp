_updater = None

class Updater():

    def __init__(self):
        self.loop = None

    def _redraw(self, *args):
        if self.need_update:
            self.need_update = False
            self.loop.draw_screen()

    def update(self):
        loop = self.loop

        if loop:
            self.need_update = True
            loop.set_alarm_in(0, self._redraw)

def update():
    get_updater().update()

def get_updater():
    global _updater
    if _updater == None:
        _updater = Updater()

    return _updater
