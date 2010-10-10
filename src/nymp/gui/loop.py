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

_loop = None
need_update = False

class NoLoopException(Exception):
    pass

def set_loop(loop):
    global _loop
    _loop = loop

def get_loop():
    if _loop:
        return _loop
    else:
        return NoLoopException

def update():
    global need_update
    need_update = True

    loop = get_loop()

    def redraw(*args):
        global need_update

        if need_update:
            need_update = False
            loop.draw_screen()

    loop.set_alarm_in(0, redraw)

def deferred_call(wait, cb, *args):
    import logging
    logging.info("wait for %i" % wait)
    
    loop = get_loop()
    loop.set_alarm_in(wait, lambda l, a: cb(*args))

