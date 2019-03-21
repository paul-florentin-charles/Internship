# -*- coding: utf-8 -*-

import fx.path as pth

import json as js

'''
sample_name : {
    "path": sample_path,
    "wet_lst": [
        (fx_id0, wet_path0),
        (fx_id1, wet_path1),
        ...
        (fx_idn, wet_pathn)
    ]
}

"wet_lst" field is a list of tuples (fx_idk, wet_pathk),
which correspond to the id of the applied fx and the path to the resulting wet signal

OTHER VERSION

sample_name : {
    "path": sample_path,
    "wets_dir_path": wets_dir_path 
}
'''

def init_dict(dpath):
    metadata = dict()
    for fpath in pth.__list_files(dpath):
        metadata[str(fpath)] = None
    return metadata
