# -*- coding: utf-8 -*-

"""
Layer to use already very simple library *pathlib*
"""

from pathlib import Path

def __path(fpath):
    return Path(fpath)

def __suffix(fpath):
    return Path(fpath).suffix

# Doesn't work if multiple dots (e.g. tar.gz files)
def __stem(fpath):
    return Path(fpath).stem

def __name(fpath):
    return Path(fpath).name

def __parent(fpath):
    return Path(fpath).parent

def __with_name(fpath, fname):
    return Path(fpath).with_name(fname)

def __with_suffix(fpath, fsuffix):
    return Path(fpath).with_suffix(fsuffix)

