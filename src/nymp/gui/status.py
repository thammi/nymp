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

import urwid

import logging

from nymp.gui.loop import deferred_call

class FunLogHandler(logging.Handler):

    def __init__(self, out_fun):
        logging.Handler.__init__(self)

        self.out_fun = out_fun

    def emit(self, record):
        self.out_fun(record.msg)

class StatusBar(urwid.Edit):

    def __init__(self):
        urwid.Edit.__init__(self)

        self.msg_id = 0

        handler = FunLogHandler(self.flash)
        handler.setLevel(logging.DEBUG)

        logger = logging.getLogger()
        logger.addHandler(handler)

    def flash(self, msg):
        self.msg_id += 1
        deferred_call(2, self.withdraw, self.msg_id)

        self.set_edit_text(msg)

    def withdraw(self, old_id):
        if old_id == self.msg_id:
            self.set_edit_text("")

