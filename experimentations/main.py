# -*- coding: utf-8 -*-

from fx.utils import _read, _load, _export
from fx.misc import usage, mkrdir
from fx.fx import _convolve, _fx

import sys

def main():
    argc = len(sys.argv)

    if argc < 3:
        usage(__file__, ['path/to/impulse/response', 'path/to/dry/signals/dir'], ['path/to/output/dir'])

    if argc > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = mkrdir()

    impulse_response = _read(sys.argv[1])
    
    dry_signals = _load(sys.argv[2])

    wet_signals = _fx(dry_signals, impulse_response, _convolve)

    _export(wet_signals, output_dir)

if __name__ == '__main__':
    main()
