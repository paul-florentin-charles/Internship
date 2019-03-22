# -*- coding: utf-8 -*-

"""
Load any sound file
Save numpy arrays as wave files
"""

from fx.config import S_RATE, ID
from fx.misc import mkrdir, rstr 
import fx.path as pth

from pydub import AudioSegment
from scipy.io.wavfile import write
from fleep import get

import numpy as np


## Useful to avoid picking non audio files ##

def __is_audio_file(fpath):
    '''Checks wether file at <fpath> is an audio file or not'''
    if not pth.__is_file(fpath):
        return False
    
    with open(fpath, 'rb') as f:
        info = get(f.read(128))
        return info.type_matches('audio')

    return False

def __list_audio_files(path, recursively=True):
    return list(filter(__is_audio_file, pth.__list_files(path, recursively)))

## Various functions based on audio properties ##
              
def __is_mono(audio_segment):
    return audio_segment.channels == 1

def __mono(audio_segment):
    if audio_segment.channels == 2:
        return audio_segment.set_channels(1)

    return audio_segment

def __convert(audio_segment, preprocess=ID):
    return np.array(preprocess(audio_segment).get_array_of_samples())

def __normalize(npy_array, operation=ID):
    return npy_array / max(map(operation, npy_array))

## Reading and writing audio files ##

def _read(fpath):
    if __is_audio_file(fpath):
        return AudioSegment.from_file(pth.__path(fpath))

    return AudioSegment.empty()

def _load(dpath):
    audio_segments = []
    for fpath in pth.__list_files(dpath):
        if __is_audio_file(fpath):
            audio_segments.append(_read(fpath))
            
    return audio_segments

def _save(npy_array, fpath, override=True):
    if not override and pth.__exists(fpath):
        return
    
    while pth.__file_name(fpath).endswith('.'):
        fpath = pth.__with_name(fpath, pth.__file_name(fpath)[:-1])
    
    if pth.__file_extension(fpath) != '.wav':
        fpath = pth.__with_extension(fpath, '.wav')

    write(fpath, S_RATE, npy_array)

def _export(npy_arrays, outdpath=None, override=True):
    if outdpath is None:
        outdpath = mkrdir()

    for idx, npy_array in enumerate(npy_arrays):
        _save(npy_array, pth.__join_path(outdpath, ''.join([str(idx), '_', rstr()])), override)

