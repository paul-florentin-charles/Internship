# -*- coding: utf-8 -*-

from src.path import __stem, __with_name
from src.utils import _load, _save, usage
from src.fx import _convolve

import sys

def main():
    argc = len(sys.argv)

    if argc < 3:
        usage(sys.argv[0], ['path/to/dry/signal', 'path/to/impulse/response'], ['path/to/wet/signal'])
        
    dry, reverb = _load(sys.argv[1]), _load(sys.argv[2])
    wet = _convolve(dry, reverb)
    _save(wet, __with_name(sys.argv[1], ''.join([__stem(sys.argv[1]), '_wet'])) if argc == 3 else sys.argv[3])

if __name__ == '__main__':
    main()
