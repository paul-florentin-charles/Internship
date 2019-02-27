"""
Adapted from : https://github.com/tensorflow/magenta-demos/blob/master/jupyter-notebooks/NSynth.ipynb (Part 1 & 2)
"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen
from skimage.transform import resize

def usage():
    print("Usage: python3 nsynth.py <path_to_audio_file> <path_to_model>")

if len(sys.argv) < 3:
    usage()
    raise SystemExit

## Utils ##

def get_extension(_file):
    '''
    Takes a string <_file>
    Returns string stripped of the characters before its last point (included), if it has any. Otherwise, returns the same string
    '''
    return _file[_file.rfind('.') + 1:]

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

def timestretch(encoding, factor):
    '''
    Normalization of <encoding>
    Followed by a stretching of time dimension by <factor>
    '''
    min_encoding, max_encoding = encoding.min(), encoding.max()
    encoding = (encoding - min_encoding) / (max_encoding - min_encoding)
    timestretches = []
    for el in encoding:
        stretched = resize(el, (int(el.shape[0] * factor), el.shape[1]), mode='reflect')
        stretched = stretched * (max_encoding - min_encoding) + min_encoding
        timestretches.append(stretched)
    return np.array(timestretches)

## Variables ##

sample_rate = 16000 # try with 44100
sample_length = 40000

_file, _model = sys.argv[1], sys.argv[2]

plot = False
debug = True

## Process ##

# loading & encoding #
audio, encoding = load_encoding(_file, sample_length, sample_rate, _model)
np.save(without_extension(_file) + '.npy', encoding)
print("(batch_size, time_steps, dimensions) :", encoding.shape)

# plotting #
if plot:
    fig, axs = plt.subplots(2, 1, figsize=(10, 5))
    axs[0].plot(audio);
    axs[0].set_title('Audio Signal')
    axs[1].plot(encoding[0]);
    axs[1].set_title('NSynth Encoding')

# decoding #
'''Synthesizes audio from the encoding and saves it'''
fastgen.synthesize(encoding, save_paths=[without_extension(_file) + "_decoded." + get_extension(_file)], samples_per_save=sample_length)

if debug:
    print("\n*****\nCongratulations, you've made it through part one\n*****\n")


# slower and faster encoding #
encoding_slower = timestretch(encoding, 1.5)
encoding_faster = timestretch(encoding, 0.5)

if plot:
    fig, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True, sharey=True)
    axs[0].plot(encoding[0]);
    axs[0].set_title('Encoding (Normal Speed)')
    axs[1].plot(encoding_faster[0]);
    axs[1].set_title('Encoding (Faster))')
    axs[2].plot(encoding_slower[0]);
    axs[2].set_title('Encoding (Slower)')

# Slower and faster decoding
fastgen.synthesize(encoding_slower, save_paths=["decoded_slower_" + _file], samples_per_save=sample_length)
fastgen.synthesize(encoding_faster, save_paths=["decoded_faster_" + _file], samples_per_save=sample_length)

if debug:
    print("\n*****\nCongratulations, you've made it through part two\n*****\n")
