"""
Taken from : https://github.com/tensorflow/magenta-demos/blob/master/jupyter-notebooks/NSynth.ipynb
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

## Part 1 ##

''' LOADING ORIGINAL SONG'''
# from https://www.freesound.org/people/MustardPlug/sounds/395058/, or pick any other wav song you wish
fname = '395058__mustardplug__breakbeat-hiphop-a4-4bar-96bpm.wav'
sr = 16000 # why not 44100
# resamples signal to <sr> and truncate it to <sample_length> elements
audio = utils.load_audio(fname, sample_length=40000, sr=sr)
#  amount of loaded samples
sample_length = audio.shape[0]
print('{} samples, {} seconds'.format(sample_length, sample_length / float(sr)))

''' ENCODING '''
# name of selected model
model_name = 'model.ckpt_200000'
encoding = fastgen.encode(audio, model_name, sample_length)
print(encoding.shape)
np.save(fname[:-4] + '.npy', encoding) # saving array

''' PLOTTING '''
fig, axs = plt.subplots(2, 1, figsize=(10, 5))
axs[0].plot(audio);
axs[0].set_title('Audio Signal')
axs[1].plot(encoding[0]);
axs[1].set_title('NSynth Encoding')

''' DECODING '''
fastgen.synthesize(encoding, save_paths=['generated_' + fname], samples_per_save=sample_length)

''' LOADING GENERATED SONG'''
synthesis = utils.load_audio('generated_' + fname, sample_length=sample_length, sr=sr)

## Part 2 ##

# use image interpolation to stretch the encoding: (pip install scikit-image)
from skimage.transform import resize

def timestretch(encodings, factor):
    min_encoding, max_encoding = encoding.min(), encoding.max()
    encodings_norm = (encodings - min_encoding) / (max_encoding - min_encoding)
    timestretches = []
    for encoding_i in encodings_norm:
        stretched = resize(encoding_i, (int(encoding_i.shape[0] * factor), encoding_i.shape[1]), mode='reflect')
        stretched = (stretched * (max_encoding - min_encoding)) + min_encoding
        timestretches.append(stretched)
    return np.array(timestretches)

def load_encoding(fname, sample_length=None, sr=16000, ckpt='model.ckpt-200000'):
    audio = utils.load_audio(fname, sample_length=sample_length, sr=sr)
    encoding = fastgen.encode(audio, ckpt, sample_length)
    return audio, encoding

''' LOADING + ENCODING ORIGINAL SONG'''
# from https://www.freesound.org/people/MustardPlug/sounds/395058/
#fname = '395058__mustardplug__breakbeat-hiphop-a4-4bar-96bpm.wav'
#sample_length = 40000
audio, encoding = load_encoding(fname, sample_length)

# Slower and faster encoding
encoding_slower = timestretch(encoding, 1.5)
encoding_faster = timestretch(encoding, 0.5)

''' PLOTTING '''
fig, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True, sharey=True)
axs[0].plot(encoding[0]);
axs[0].set_title('Encoding (Normal Speed)')
axs[1].plot(encoding_faster[0]);
axs[1].set_title('Encoding (Faster))')
axs[2].plot(encoding_slower[0]);
axs[2].set_title('Encoding (Slower)')

''' DECODING '''
fastgen.synthesize(encoding_faster, save_paths=['generated_faster_' + fname])
fastgen.synthesize(encoding_slower, save_paths=['generated_slower_' + fname])

''' LOADING GENERATED SONGS'''
audio_fast = utils.load_audio('generated_faster_' + fname, sample_length=None, sr=sr)
audio_slow = utils.load_audio('generated_slower_' + fname, sample_length=None, sr=sr)

## Part 3 ##

# TODO
