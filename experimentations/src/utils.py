# -*- coding: utf-8 -*-

"""
Load any sound file
Save numpy arrays as wave files
"""

from src.colors import *
from src.config import S_RATE
from src.path import __name, __path, __suffix, __with_name, __with_suffix
# TODO: For some reason [from import *] doesn't work
#from src.path import *

from pydub import AudioSegment
from scipy.io.wavfile import write

import numpy as np

def __mono(audio_segment):
    if audio_segment.channels == 2:
        return audio_segment.set_channels(1)
    return audio_segment

def __normalized(audio_segment):
    return np.array(audio_segment.get_array_of_samples()) / audio_segment.max

def _load(fpath):
    return AudioSegment.from_file(__path(fpath))

def _save(npy_array, fpath):
    while __name(fpath).endswith('.'):
        fpath = __with_name(fpath, __name(fpath)[:-1])
    
    if __suffix(fpath) != '.wav':
        fpath = __with_suffix(fpath, '.wav')

    write(fpath, S_RATE, npy_array)

