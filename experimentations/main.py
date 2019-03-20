# -*- coding: utf-8 -*-

from src.path import __list_files, __join_path, __stem
from src.utils import _load, _save
from src.misc import usage, mkrdir
from src.fx import _convolve

import sys

def main():
    argc = len(sys.argv)

    if argc < 3:
        usage(__file__, ['path/to/impulse/response', 'path/to/dry/signals/dir'], ['path/to/output/dir'])

    if argc > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = mkrdir()

    impulse_response = _load(sys.argv[1])

    for fpath in __list_files(sys.argv[2]):
        dry = _load(fpath)
        wet = _convolve(dry, impulse_response)
        _save(wet, __join_path(output_dir, ''.join([__stem(fpath), '_wet'])))

if __name__ == '__main__':
    main()
