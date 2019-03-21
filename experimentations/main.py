#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fx.utils import _load, _export
from fx.metadata import init_dict
from fx.misc import usage, mkrdir
from fx.fx import _fxs

import sys

def main():
    argc = len(sys.argv)

    if argc < 3:
        usage(__file__.replace('./', ''), ['path/to/impulse/responses/dir', 'path/to/dry/signals/dir'], ['path/to/output/dir'])

    if argc > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = mkrdir()

    metadata = init_dict(sys.argv[2])
    print(metadata)

    impulse_responses, dry_signals = _load(sys.argv[1]), _load(sys.argv[2])
    
    for idx, dry in enumerate(dry_signals):
        wet_signals = _fxs(dry, impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        _export(wet_signals, dpath)

if __name__ == '__main__':
    main()
