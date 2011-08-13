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
        config = defaults[name]
        save_config(name, config)
        return config
    else:
        return {}

def save_config(name, data):
    fn = os.path.join(CONF_DIR, name + ".json")

    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR)

    f = open(fn, 'w')
    json.dump(data, f, sort_keys=True, indent=4)
    f.close()

