# -*- coding: utf-8 -*-

from fx.colors import bright, magenta_fg, cyan_fg
from fx.config import CHRS, SIZE
from fx.path import __is_file, __path_exists, __make_dir, __join_path, __create_file

from random import choice

import fleep as fl

class NotAudioFile(Exception):
    pass

def usage(pname, required_args = [], optional_args = []):
    raise SystemExit(''.join([bright('Usage:'), magenta_fg(' python3 '), cyan_fg(pname), ' ', ' '.join(required_args), ' ', ' '.join([''.join(['[', arg, ']']) for arg in optional_args])]))

def is_audio_file(fpath):
    if not __is_file(fpath):
        raise FileNotFoundError
    
    with open(fpath, 'rb') as f:
        info = fl.get(f.read(128))

    return info.type_matches('audio')

def rstr(size=SIZE, chars=CHRS):
    '''Generates a random string of size <size> containing chars from <chars>'''
    return ''.join(choice(chars) for _ in range(size))

def mkrdir(path='.'):
    dpath = __join_path(path, rstr())
    while(__path_exists(dpath)):
        dpath = __join_path(path, rstr())
    __make_dir(dpath)
    return dpath

def mkrfile(path='.'):
    fpath = __join_path(path, rstr())
    while(__path_exists(fpath)):
        fpath = __join_path(path, rstr())
    __create_file(fpath)
    return fpath
