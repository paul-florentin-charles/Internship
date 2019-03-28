# -*- coding: utf-8 -*-

import json


def _dump(fpath, _dict, mode='w', n_ident=4):
    with open(fpath, mode) as fjson:
        json.dump(_dict, fjson, indent=n_ident)

def _load(fpath):
    with open(fpath, 'r') as fjson:
        return json.load(fjson)
        
def _write(_dict, field, value, override=True):
    if override or field not in _dict:
        _dict[field] = value    
