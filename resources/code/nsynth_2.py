"""
Adapted from : https://github.com/tensorflow/magenta-demos/blob/master/jupyter-notebooks/NSynth.ipynb (Part 3)
"""

import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

def usage():
    print("Usage: python3 nsynth.py <path_to_audio_file> <path_to_audio_file> <path_to_model>")

if len(sys.argv) < 4:
    usage()
    raise SystemExit

## Utils ##

def without_extension(_file):
    '''
    Takes a string <_file>
    Returns string stripped of the characters after its last point (included), if it has any. Otherwise, returns the same string
    '''
    return _file[:_file.rfind('.')]

def load_encoding(_file, sample_length=None, sample_rate=16000, ckpt='model.ckpt-200000'):
    '''
    Resamples signal to <sample_rate> and truncates it to <sample_length> elements
    Then encodes it through the model <ckpt>
    Returns a tuple (signal, encoded_signal)
    '''
    audio = utils.load_audio(_file, sample_length=sample_length, sr=sample_rate)
    encoding = fastgen.encode(audio, ckpt, sample_length)
    return audio, encoding

# Hanning window
def fade(encoding, mode='in'):
    length = encoding.shape[1]
    fadein = (0.5 * (1.0 - np.cos(math.pi * np.arange(length) / float(length)))).reshape(1, -1, 1)
    return encoding * (fadein if mode == 'in' else (1.0 - fadein))

# Fade out + Fade in
def crossfade(encoding1, encoding2):
    return fade(encoding1, 'out') + fade(encoding2, 'in')

## Variables ##

sample_rate = 16000 # try with 44100
sample_length = 80000

_file_1, _file_2, _model = sys.argv[1], sys.argv[2], sys.argv[3]

plot = False
debug = True

## Process ##

# loading & encoding #
audio_1, encoding_1 = load_encoding(_file_1, sample_length, sample_rate, _model)
audio_2, encoding_2 = load_encoding(_file_2, sample_length, sample_rate, _model)
np.save(without_extension(_file_1) + '.npy', encoding_1)
np.save(without_extension(_file_2) + '.npy', encoding_2)
print("1. (batch_size, time_steps, dimensions) :", encoding_1.shape)
print("2. (batch_size, time_steps, dimensions) :", encoding_2.shape)

# mixing encodings #
encoding_mix = (encoding_1 + encoding_2) / 2.0

if plot:
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    axs[0].plot(encoding_1[0]);
    axs[0].set_title('Encoding 1')
    axs[1].plot(encoding_2[0]);
    axs[1].set_title('Encoding 2')
    axs[2].plot(encoding__mix[0]);
    axs[2].set_title('Average')

# Decoding mixed encoding
fastgen.synthesize(encoding_mix, save_paths=['decoded_mix.wav'])

if plot:
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    axs[0].plot(encoding_1[0]);
    axs[0].set_title('Original Encoding')
    axs[1].plot(fade(encoding_1, 'in')[0]);
    axs[1].set_title('Fade In')
    axs[2].plot(fade(encoding_1, 'out')[0]);
    axs[2].set_title('Fade Out')

if plot:
    fig, axs = plt.subplots(3, 1, figsize=(10, 7))
    axs[0].plot(encoding_1[0]);
    axs[0].set_title('Encoding 1')
    axs[1].plot(encoding_2[0]);
    axs[1].set_title('Encoding 2')
    axs[2].plot(crossfade(encoding_1, encoding_2)[0]);
    axs[2].set_title('Crossfade')

# Decoding crossfaded encoding
fastgen.synthesize(crossfade(enc1, enc2), save_paths=['decoded_crossfade.wav'])

if debug:
    print("\n*****\nCongratulations, you've made it through part three\n*****\n")
