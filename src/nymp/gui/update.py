##############################################################################
##
##  nymp - a graphical xmms2 cli frontend
##  Copyright 2010 Thammi
##
##  nymp is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  nymp is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with nymp.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

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
