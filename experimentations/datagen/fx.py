# -*- coding: utf-8 -*-

"""
Apply fx to a dry sound
"""

from datagen.config import CONV_MOD
from datagen.utils import __is_mono, __mono, __convert, __normalize

from scipy.signal import convolve


def _convolve(dry, fx):
    if __is_mono(dry) or __is_mono(fx):
        _dry, _fx = __convert(dry, __mono), __convert(fx, __mono)
        _dry, _fx = __normalize(_dry), __normalize(_fx)
    else:
        _dry, _fx = __convert(dry), __convert(fx)
        _dry, _fx = __normalize(_dry, sum), __normalize(_fx, sum)

    # Give a 'float64' numpy array
    # TODO: Convert to 'int16' without ruining the signal
    # TODO: mode='same' keeps stereo but gives distortion
    conv = convolve(_dry, _fx, mode=CONV_MOD)

    """
    conv = conv / max(conv)
    conv = conv * (2**15 - 1)
    conv.dtype = 'int16'
    """
    
    return conv

def _apply_fxs(dry, fxs, func=_convolve):
    wet_signals = []
    
    if dry.frame_count() == 0:
        return wet_signals
    
    for fx in fxs:
        wet_signals.append(func(dry, fx))
    
    return wet_signals
