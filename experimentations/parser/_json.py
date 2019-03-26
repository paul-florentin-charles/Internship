# -*- coding: utf-8 -*-

import json

def _dump(fpath, _dict, mode='a', n_ident=4):
    with open(fpath, mode) as fjson:
        json.dump(_dict, fjson, indent=n_ident)

def _write(_dict, field, value, override=True):
    if override or field not in _dict:
        _dict[field] = value

def _reset(_dict):
    _dict = dict()
        
