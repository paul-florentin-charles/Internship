#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datagen.config import JSON_FNAME, SAVE_STEPS
from datagen.utils import _load, _export, _read, __list_audio_files
from datagen.misc import usage, mkrdir
from datagen.fx import _apply_fxs

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

    with open(JSON_FNAME, 'w'): pass
    
    info = dict()
        
    for idx, dryfpath in enumerate(__list_audio_files(sys.argv[2])):
        wet_signals = _apply_fxs(_read(dryfpath), impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        info[str(dryfpath)] = str(dpath)
        _export(wet_signals, dpath)
        if (idx + 1) % SAVE_STEPS == 0:
            with open(JSON_FNAME, 'a') as fjson:
                json.dump(info, fjson, indent=4)
            info = dict()

    with open(JSON_FNAME, 'a') as fjson:
        json.dump(info, fjson, indent=4)

if __name__ == '__main__':
    main()
