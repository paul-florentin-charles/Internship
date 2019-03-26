#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datagen.utils import _load, _export, _read, __list_audio_files
from datagen.misc import usage, mkrdir
from datagen.fx import _apply_fxs
import parser._json as pjsn
import parser._toml as ptml

import sys

def main():
    argc = len(sys.argv)

    if argc < 3:
        raise SystemExit(usage(__file__.replace('./', ''), ['path/to/impulse/responses/dir', 'path/to/dry/signals/dir'], ['path/to/output/dir']))

    if argc > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = mkrdir()

    impulse_responses = _load(sys.argv[1])

    open(ptml.value('meta', 'json_fname'), 'w').close()
    
    info = dict()
        
    for idx, dryfpath in enumerate(__list_audio_files(sys.argv[2])):
        wet_signals = _apply_fxs(_read(dryfpath), impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        _export(wet_signals, dpath)

        pjsn._write(info, str(dryfpath), str(dpath))
        
        if (idx + 1) % ptml.value('meta', 'save_steps') == 0:
            pjsn._dump(ptml.value('meta', 'json_fname'), info)
            pjsn._reset(info)

    pjsn._dump(ptml.value('meta', 'json_fname'), info)

if __name__ == '__main__':
    main()
