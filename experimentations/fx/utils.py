# -*- coding: utf-8 -*-

"""
Load any sound file
Save numpy arrays as wave files
"""

from fx.config import S_RATE
from fx.misc import is_audio_file, NotAudioFile, mkrdir, rstr 
from fx.path import __path, __file_name, __file_extension, __path_exists, __with_name, __with_extension, __join_path, __list_files
# TODO: For some reason [from import *] doesn't work
#from fx.path import *

from pydub import AudioSegment
from scipy.io.wavfile import write

def __is_mono(audio_segment):
    return audio_segment.channels == 1

def __mono(audio_segment):
    if audio_segment.channels == 2:
        return audio_segment.set_channels(1)
    return audio_segment

def _read(fpath):
    if is_audio_file(fpath):
        return AudioSegment.from_file(__path(fpath))
    raise NotAudioFile

def _load(dpath):
    audio_segments = []
    for fpath in __list_files(dpath):
        audio_segments.append(_read(fpath))
    return audio_segments

def _save(npy_array, fpath, override=True):
    if not override and __path_exists(fpath):
        return
    
    while __file_name(fpath).endswith('.'):
        fpath = __with_name(fpath, __file_name(fpath)[:-1])
    
    if __file_extension(fpath) != '.wav':
        fpath = __with_extension(fpath, '.wav')

    write(fpath, S_RATE, npy_array)

def _export(npy_arrays, outdpath=None, override=True):
    if outdpath is None:
        outdpath = mkrdir()

    for idx, npy_array in enumerate(npy_arrays):
        _save(npy_array, __join_path(outdpath, ''.join([str(idx), '_', rstr()])), override)
    
