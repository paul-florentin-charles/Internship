# -*- coding: utf-8 -*-

# Hyperparameters #

## DCGAN ##

### Generator ###

g_learning_rate = 2e-4
g_batch_size = 64
g_stride = 4

### Discriminator ###

d_learning_rate = 2e-4
d_batch_size = 64
d_stride = 4

## Audio ##

sample_rate = 16000 #44100
sample_duration = 3 # seconds
sample_length = sample_rate * sample_duration

frame_size = 1024
hop_size = 256
n_freq_bins = 256


