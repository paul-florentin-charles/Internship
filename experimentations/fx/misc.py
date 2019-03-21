# -*- coding: utf-8 -*-

from fx.colors import bright, magenta, cyan
from fx.config import CHRS, SIZE
import fx.path as pth

from random import choice

import fleep as fl

class NotAudioFile(Exception):
    pass

def usage(pname, required_args = [], optional_args = []):
    return ''.join([bright('Usage:'), magenta(' python3 '), cyan(pname), ' ', ' '.join(required_args), ' ', ' '.join([''.join(['[', arg, ']']) for arg in optional_args])])

def is_audio_file(fpath):
    if not pth.__is_file(fpath):
        raise FileNotFoundError
    
    with open(fpath, 'rb') as f:
        info = fl.get(f.read(128))

    return info.type_matches('audio')

def rstr(size=SIZE, chars=CHRS):
    '''Generates a random string of size <size> containing chars from <chars>'''
    return ''.join(choice(chars) for _ in range(size))

def mkrdir(path='.', prefix=''):
    dpath = pth.__join_path(path, ''.join([prefix, rstr()]))
    while(pth.__exists(dpath)):
        dpath = pth.__join_path(path, ''.join([prefix, rstr()]))
    pth.__make_dir(dpath)
    return dpath
