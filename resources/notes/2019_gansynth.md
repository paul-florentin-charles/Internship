# GANSynth: Adversarial Audio Synthesis


## Introduction

State of the art: WaveNet-based models *e.g.* autoregressive models
* Fine scale : sample by sample
* Relies on external conditioning for wider scales
* Slow : one sample at a time + depends on all previous ones in a window
* Autoencoder derivatives are constrained to short duration to model latent space

GANs
- Effective at generating hi-res images
- Parralel sampling
- Global conditioning 
- Architectures for images can be adapted to audio
- However, doesn't have the same perceptual quality

### Generating instrument timbres

The idea for GANs is to used specific datasets and then broaden their diversity. <br>
This principle has been applied to build NSynth, which contains only notes of identical durations, with specific free characteristics. <br>
Moreover, each note is associated with a list of labels to allow conditioning.

Contrarily to autoregressive WaveNet models and spectrogram autoencoders, where causal convolutions are present.

### Audio representations

Most audio waveforms contains periodicity, represented by frequencies. <br>
Convolutional filters typically learn to form filter banks centered around these frequencies, with a log post (mu-law for instance) processing to suit human's perception.

Human perception is very sensitive to irregularities. <br>
Yet, when applying STFT or other frame-based algorithms, there is often a phase disalignment. <br>
Indeed, the hop size or stride doesn't necessarily correspond to the frequency, inducing a shift.

However, since this shift increases in a constant manner, its derivative is a constant. <br>
This allows a quantity called *instantaneous frequency*, derivative of the *unwrapped phase* in function of the time. 

Below is an example for a pure sine wave.

![Phase Representation](https://gitgud.io/polochinoc/internship/raw/master/resources/notes/images/gansynth_phase.png)

### Contributions

* Generating log-mag spectrograms with phase using GANs
- Instaneous frequency is more effective than phase
- Separate harmonics : either increase stride and switch to mel scale improve performance
- 54 000 times faster than WaveNet baseline
- Consistent timbre using global latent and pitch vectors


## Experiments

### Dataset

NSynth dataset, restricted to acoustic instruments with fundamentals ranging from 32 to 1000 Hz. <br>
This infers about 70 000 notes.

### Architecture and representations

Adapting progressive GAN to generate audio spectra. <br>
Generative model input is a random vector obtained from **Spherical Gaussian**. <br>
It is then run through transposed convolution layers to be upsampled, then downsampled through convolutions from the discriminator (symmetrical to the generator model). <br>
Usage of **gradient penalty** and **pixel normalization** for each layer.

Both progressive and not progressive GANs are tested, but progressive show better results. <br>
Progressive means the discriminator learns while being fed by the generator.

One-hot encoding of pitch is concatenated to the latent vector to achieve independent control of pitch and timbre. <br>
A supplementary loss on pitch label prediction is added to the discriminator to foster it.

Spectral representation :
* Compute STFT mag and phases angles : 256 stride, 1024 frame size --> 513 freq bins
* Remove one freq to get a (256, 512, 2) array, 2 since there are phase and magnitude
* Take log of mag, and rescale it to be in [-1,1] to make full usage of *tanh* activation
* Phase angle likewise scaled between -1 and 1
* Optionally, phase is unwrapped to get instantaneous frequency with a simple operation
* Low freq range needs better resolution :
    * frame/hop size are doubled for images with size (128, 1024, 2)
    * mel frequency scale for both magnitudes and IF (instantaneous frequencies) 

WaveGAN is adapated to accept pitch conditioning, so it can be used as a baseline for comparison with GANSynth. <br>
Furthermore, even WaveNet is modified to accept pitch encoding, to be compared with GANSynth.


## Metrics

- Human Evaluation : Based on a 5-level notation scale
- Number of Statistically-Different Bins (NDB) : Diversity of generated sounds using kmeans clusterisation of training examples and generated examples in spectrogram space, then measuring how they are related to each other.
- Inception Score (IS) : Pre-trained Inception classifier ; IS = **mean KL divergence** between the output probability vector of the classifier and the marginal distribution of the input
In a nutshell, IS penalizes models with ambiguous examples classification and models with examples mapped to a few classes of the classifier. 
- Pitch Accuracy (PA) & Pitch Entropy (PE) : Accuracy of a pitch classifier on examples, and entropy of the output distribution
- Fréchet Inception Distance (FID) : `not clear at all to me, need to review`

## Results

*Check paper*

## Qualitative Analysis

Listen to audio examples [here](https://storage.googleapis.com/magentadata/papers/gansynth/index.html "GANSynth Audio Examples")

TODO : Complete this part

### Phase coherence

### Interpolation

### Consistent timbre across pitch
