# -*- coding: utf-8 -*-

import toml

def _value(fpath, section, vname):
    _dict = toml.load(fpath)
    if section in _dict and vname in _dict[section]:
        return _dict[section][vname]
    return None

def value(section, vname):
    return _value('config.toml', section, vname)
