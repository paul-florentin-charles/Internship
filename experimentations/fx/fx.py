# -*- coding: utf-8 -*-

"""
Apply fx to a dry sound
"""

from fx.config import CONV_MOD
from fx.utils import __is_mono, __mono

from scipy.signal import convolve

import numpy as np

def _convolve(dry, fx):
    if __is_mono(dry) or __is_mono(fx):
        _dry = np.array(__mono(dry).get_array_of_samples())
        _fx = np.array(__mono(fx).get_array_of_samples())
    else:
        _dry = np.array(dry.get_array_of_samples()).reshape(-1, 2)
        _fx = np.array(fx.get_array_of_samples()).reshape(-1, 2)

    # Give a 'float64' numpy array
    # TODO: Convert to 'int16' without ruining the signal
    # TODO: mode='same' keeps stereo but gives distortion
    conv = convolve(_dry / dry.max, _fx / fx.max, mode=CONV_MOD)
    return conv

def _fxs(dry, fxs, func=_convolve):
    wet_signals = []
    for fx in fxs:
        wet_signals.append(func(dry, fx))
    return wet_signals
