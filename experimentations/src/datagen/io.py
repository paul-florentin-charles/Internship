# -*- coding: utf-8 -*-

"""
Load any sound file
Save numpy arrays as wave files
"""

from src.datagen.utils import __list_audio_files, __is_audio_file
from src.datagen.fx import _apply_fxs
from src.utils.tools import mkrdir, rstr 
import src.utils.path as pth
import src.parser.toml as tml, src.parser.json as jsn

from pydub import AudioSegment
from scipy.io.wavfile import write


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

    write(fpath, tml.value('audio', 's_rate'), npy_array)

def _export(npy_arrays, outdpath=None, override=True):
    if outdpath is None:
        outdpath = mkrdir()

    for idx, npy_array in enumerate(npy_arrays):
        _save(npy_array, pth.__join_path(outdpath, ''.join([str(idx), '_', rstr()])), override)

## Generating dataset ##

def generate_dataset(dry_dpath, fx_dpath, output_dir, func=None):
    if not pth.__exists(output_dir):
        pth.__make_dir(output_dir)

    fxs = _load(fx_dpath)

    pth.__create_file(tml.value('meta', 'json_fname'))

    info = dict()
        
    for idx, dryfpath in enumerate(__list_audio_files(dry_dpath)):
        if func:
            wet_signals = _apply_fxs(_read(dryfpath), fxs, func)
        else:
            wet_signals = _apply_fxs(_read(dryfpath), fxs)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        _export(wet_signals, dpath)
        
        info[str(dryfpath)] = str(dpath)
        if (idx + 1) % tml.value('meta', 'save_steps') == 0:
            jsn._dump(tml.value('meta', 'json_fname'), info)

    jsn._dump(tml.value('meta', 'json_fname'), info)

    return info
