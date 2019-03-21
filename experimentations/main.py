#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fx.config import JSON_FNAME
from fx.utils import _load, _export, _read
from fx.misc import usage, mkrdir
from fx.fx import _fxs
import fx.path as pth

import sys, json

def main():
    argc = len(sys.argv)

    if argc < 3:
        raise SystemExit(usage(__file__.replace('./', ''), ['path/to/impulse/responses/dir', 'path/to/dry/signals/dir'], ['path/to/output/dir']))

    if argc > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = mkrdir()

    impulse_responses = _load(sys.argv[1])

    info = dict()
    for idx, fpath in enumerate(pth.__list_files(sys.argv[2])):
        wet_signals = _fxs(_read(fpath), impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        info[str(fpath)] = str(dpath)
        _export(wet_signals, dpath)

    with open(JSON_FNAME, 'w') as fjson:
        json.dump(info, fjson, indent=4)

if __name__ == '__main__':
    main()
