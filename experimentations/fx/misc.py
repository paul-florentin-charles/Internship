# -*- coding: utf-8 -*-

from src.colors import *
from src.config import CHRS, SIZE
from src.path import __is_file, __exists, __mkdir, __join_path

from random import choice
from fleep import get

class NotAudioFile(Exception):
    pass

def usage(pname, required_args = [], optional_args = []):
    raise SystemExit(''.join([bright('Usage:'), magenta_fg(' python3 '), cyan_fg(pname), ' ', ' '.join(required_args), ' ', ' '.join([''.join(['[', arg, ']']) for arg in optional_args])]))

def is_audio_file(fpath):
    if not __is_file(fpath):
        raise FileNotFoundError
    
    with open(fpath, 'rb') as f:
        info = get(f.read(128))

    return info.type_matches('audio')

def rstr(size=SIZE, chars=CHRS):
    '''Generates a random string of size <size> containing chars from <chars>'''
    return ''.join(choice(chars) for _ in range(size))

def mkrdir(path='.'):
    dpath = __join_path(path, rstr())
    while(__exists(dpath)):
        dpath = __join_path(dpath, rstr())
    __mkdir(dpath)
    return dpath
