# -*- coding: utf-8 -*-

import parser._toml as ptml
import parser._json as pjsn
from datagen.utils import _read, _load, __mono, __convert

from random import choice
import numpy as np


# TODO: I could use asarray as well, idk
def retrieve_data(preprocess=__mono, _type=None):
    _dict = pjsn._load(ptml.value('meta', 'json_fname'))

    data, labels = [np.zeros(ptml.value('audio', 's_len'), dtype='int')] * 2
    for key in _dict:
        data = np.vstack((data, __convert(choice(_load(_dict[key])), preprocess, _type)))
        labels = np.vstack((labels, __convert(_read(key), preprocess, _type)))
    
    return np.delete(data, 0, 0), np.delete(labels, 0, 0)
        
