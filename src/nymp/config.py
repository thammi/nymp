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

def load_config(name):
    fn = os.path.join(CONF_DIR, name + ".json")

    if os.path.exists(fn): 
        try:
            f = open(fn, 'r')
            cache[name] = json.load(f)
        except:
            logging.exception("Unable to load configuration")
            cache[name] = None
        finally:
            f.close()
    else:
        cache[name] = None

def get_config(name):
    if name not in cache:
        load_config(name)

    if name in cache and cache[name] != None:
        return cache[name]
    else:
        return load_default(name)

def load_default(name):
    if name in defaults:
        return defaults[name]
    else:
        return None

def save_config(name, data):
    fn = os.path.join(CONF_DIR, name + ".json")

    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR)

    f = open(fn, 'w')
    json.dump(data, f, sort_keys=True, indent=4)
    f.close()

