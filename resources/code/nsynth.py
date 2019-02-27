"""
Taken from : https://github.com/tensorflow/magenta-demos/blob/master/jupyter-notebooks/NSynth.ipynb
"""

import os, sys
import numpy as np
import matplotlib.pyplot as plt
from magenta.models.nsynth import utils
from magenta.models.nsynth.wavenet import fastgen

## Part 1 ##

''' LOADING ORIGINAL SONG'''
if len(sys.argv) < 2:
    raise SystemExit
fname = sys.argv[1]
sr = 16000 # try with 44100
sample_length = 40000
# resamples signal to <sr> and truncate it to <sample_length> elements
audio = utils.load_audio(fname, sample_length=sample_length, sr=sr)
assert(sample_length == audio.shape[0])
print('{} samples, {} seconds'.format(sample_length, sample_length / float(sr)))

''' ENCODING '''
model_name = 'model.ckpt_200000'
encoding = fastgen.encode(audio, model_name, sample_length)
print(encoding.shape)
np.save(fname + '.npy', encoding) # saving array

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

print("\n*****\nCongratulations, you've made it through part one\n*****\n")

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
fname = "new_song.wav"
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

sample_length = 80000
fname_1, fname_2 = "song1.wav", "song2.wav"

aud1, enc1 = load_encoding(fname_1, sample_length)
aud2, enc2 = load_encoding(fname_2, sample_length)

enc_mix = (enc1 + enc2) / 2.0

fig, axs = plt.subplots(3, 1, figsize=(10, 7))
axs[0].plot(enc1[0]);
axs[0].set_title('Encoding 1')
axs[1].plot(enc2[0]);
axs[1].set_title('Encoding 2')
axs[2].plot(enc_mix[0]);
axs[2].set_title('Average')

# Decoding
fastgen.synthesize(enc_mix, save_paths='mix.wav')

# Hanning window
def fade(encoding, mode='in'):
    length = encoding.shape[1]
    fadein = (0.5 * (1.0 - np.cos(3.1415 * np.arange(length) / float(length)))).reshape(1, -1, 1)
    if mode == 'in':
        return fadein * encoding
    else:
        return (1.0 - fadein) * encoding
    
fig, axs = plt.subplots(3, 1, figsize=(10, 7))
axs[0].plot(enc1[0]);
axs[0].set_title('Original Encoding')
axs[1].plot(fade(enc1, 'in')[0]);
axs[1].set_title('Fade In')
axs[2].plot(fade(enc1, 'out')[0]);
axs[2].set_title('Fade Out')

# Fade out + Fade in
def crossfade(encoding1, encoding2):
    return fade(encoding1, 'out') + fade(encoding2, 'in')

fig, axs = plt.subplots(3, 1, figsize=(10, 7))
axs[0].plot(enc1[0]);
axs[0].set_title('Encoding 1')
axs[1].plot(enc2[0]);
axs[1].set_title('Encoding 2')
axs[2].plot(crossfade(enc1, enc2)[0]);
axs[2].set_title('Crossfade')

# Decoding
fastgen.synthesize(crossfade(enc1, enc2), save_paths=['crossfade.wav'])
