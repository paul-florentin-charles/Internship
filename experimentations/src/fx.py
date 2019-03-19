# -*- coding: utf-8 -*-

"""
Apply fx to a dry sound
"""

from src.utils import __mono, __normalized

from scipy.signal import convolve

def _convolve(dry, fx):
    # Temporary solution
    # TODO: adapt to stereo signals
    dry, fx = __mono(dry), __mono(fx)

    # Give a 'float64' numpy array
    # TODO: Convert to 'int16' without ruining the signal
    return convolve(__normalized(dry), __normalized(fx))
