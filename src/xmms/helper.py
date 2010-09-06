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

