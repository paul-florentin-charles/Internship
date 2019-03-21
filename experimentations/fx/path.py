# -*- coding: utf-8 -*-

"""
Layer to use already very simple library *pathlib*
Not performance optimized though
"""

from pathlib import Path

def __path(fpath):
    return Path(fpath)

def __file_extension(fpath):
    return __path(fpath).suffix

# Doesn't work if multiple dots (e.g. tar.gz files)
def __no_extension(fpath):
    return __path(fpath).stem

def __file_name(fpath):
    return __path(fpath).name

def __parent_path(fpath):
    return __path(fpath).parent

def __with_name(fpath, fname):
    return __path(fpath).with_name(fname)

def __with_extension(fpath, fextension):
    return __path(fpath).with_suffix(fextension)

def __exists(path):
    return __path(path).exists()

def __is_file(fpath):
    return __path(fpath).is_file()

def __is_dir(path):
    return __path(path).is_dir()

def __list_files(path, recursively=True):
    if __is_file(path):
        return [path]
    elif __is_dir(path):
        if recursively:
            return list(filter(__is_file, __path(path).glob('**/*')))
        else:
            return list(filter(__is_file, __path(path).iterdir()))
    return []

def __join_path(lpath, rpath):
    return __path(lpath).joinpath(__path(rpath))

def __make_dir(dpath):
    __path(dpath).mkdir()
