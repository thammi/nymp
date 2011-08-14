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

import os
import os.path

import json

from nymp.defaults import defaults

CONF_DIR = os.path.join(userconfdir_get(), "clients", "nymp")

cache = {}

def get_config(name):
    fn = os.path.join(CONF_DIR, name + ".json")

    if os.path.exists(fn): 
        try:
            f = open(fn, 'r')
            config = json.load(f)
            f.close()

            return config
        except:
            return load_defaults(name)
    else:
        return load_defaults(name)

def load_defaults(name):
    if name in defaults:
        return defaults[name]
    else:
        return {}

def save_config(name, data):
    fn = os.path.join(CONF_DIR, name + ".json")

    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR)

    f = open(fn, 'w')
    json.dump(data, f, sort_keys=True, indent=4)
    f.close()

