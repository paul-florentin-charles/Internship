# -*- coding: utf-8 -*-

"""
Apply fx to a dry sound
"""

from datagen.utils import __is_mono, __mono, __convert, __normalize, __float2pcm
import parser._toml as ptml

from scipy.signal import convolve

import numpy as np

                                                    
def _convolve(dry, fx):
    if __is_mono(dry) or __is_mono(fx):
        _dry, _fx = __convert(dry, __mono), __convert(fx, __mono)
        _dry, _fx = __normalize(_dry), __normalize(_fx)
    else:
        _dry, _fx = __convert(dry), __convert(fx)
        _dry, _fx = __normalize(_dry, sum), __normalize(_fx, sum)

    # Gives a 'float64' numpy array
    # TODO: Convert to 'int16' without ruining the signal
    # TODO: mode='same' keeps stereo but gives distortion
    _conv = convolve(_dry, _fx, mode=ptml.value('audio', 'conv_mod'))
    _conv = __normalize(_conv, sum) if _conv.ndim == 2 else __normalize(_conv)

    _conv = __float2pcm(_conv)
    
    return _conv

def _apply_fxs(dry, fxs, func=_convolve):
    wet_signals = []
    
    if dry.frame_count() == 0:
        return wet_signals
    
    for fx in fxs:
        wet_signals.append(func(dry, fx))
    
    return wet_signals
