# -*- coding: utf-8 -*-

"""
Apply fx to a dry sound
"""

from fx.config import CONV_MOD
from fx.utils import __is_mono, __mono, __convert, __normalize

from itertools import repeat
from scipy.signal import convolve


def _convolve(dry, fx):
    if __is_mono(dry) or __is_mono(fx):
        _dry, _fx = map(__convert, (dry, fx), repeat(__mono))
        _dry, _fx = map(__normalize, (_dry, _fx))
    else:
        _dry, _fx = map(__convert, (dry, fx))
        _dry, _fx = map(__normalize, (_dry, _fx), repeat(sum))

    # Give a 'float64' numpy array
    # TODO: Convert to 'int16' without ruining the signal
    # TODO: mode='same' keeps stereo but gives distortion
    conv = convolve(_dry, _fx, mode=CONV_MOD)
    
    return conv

def _apply_fxs(dry, fxs, func=_convolve):
    wet_signals = []
    
    if dry.frame_count() == 0:
        return wet_signals
    
    for fx in fxs:
        wet_signals.append(func(dry, fx))
    
    return wet_signals
