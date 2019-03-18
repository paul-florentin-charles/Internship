# -*- coding: utf-8 -*-

from os.path import basename, splitext

# Doesn't work if multiple dots (e.g. tar.gz files)
def __extensionless(fname):
    return splitext(fname)[0]

def __pathless(fpath):
    return basename(fpath)

def __mono(raw_data):
    if raw_data.ndim == 2:
        return raw_data[:, 0] + raw_data[:, 1]
    return raw_data

from scipy.io.wavfile import read, write

def _load(fpath):
    data = dict()
    
    data['sample_rate'], data['raw_data'] = read(fpath)
    data['bit_depth'] = data['raw_data'].dtype.itemsize * 8
    data['mono'] = data['raw_data'].ndim == 1
    data['sample_length'] = data['raw_data'].shape[0]
    data['name'] = __extensionless(__pathless(fpath))
    
    return data

def _write(data, extension='wav'):
    write(''.join([data['name'], '.', extension]), data['sample_rate'], data['raw_data'])


from scipy.signal import convolve

import numpy as np

def _convolve(dry_data, effect_data, name='convolution'):
    convolved_data = dict(name=name)
    
    raw_data = convolve(dry_data['raw_data'] / max(__mono(dry_data['raw_data'])), effect_data['raw_data'] / max(__mono(effect_data['raw_data'])))
    
    convolved_data['raw_data'] = raw_data
    convolved_data['sample_rate'] = dry_data['sample_rate']
    convolved_data['bit_depth'] = dry_data['raw_data'].dtype.itemsize * 8
    convolved_data['mono'] = convolved_data['raw_data'].ndim == 1
    convolved_data['sample_length'] = convolved_data['raw_data'].shape[0]
    
    return convolved_data
