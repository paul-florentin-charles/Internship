# Adversarial Audio Synthesis


## Introduction

Why GANs ?
* data augmentation
* fast
* concrete application to sound domain (*e.g.*foley artists)

First solution would be to work on spectrograms and use typical GANs used for images. <br>
Problem is that backward conversion, from spectrum to time representation, implies losses of information. <br>
This can be partially tackled by adding another model that learns inversion with supervised training, but it adds up complexity to the whole issue.

Autoregressive approaches, such as WaveNet, work on raw audio and therefore needn't any feature modelisation. <br>
However, since they are based on *causal convolutions*, they are utterly memory-hungry as each samples depends on the previous ones. <br>
It entails a pseudo-quadratic complexity (not exactly quadratic since a windows is set).

Two strategies
- SpecGAN : Building a spectrogram representation, then adapting the *DCGAN* method on it.
- WaveGAN : Modifying the *DCGAN* architecture so that it takes $1 x n$ dimension matrices.

Goal : investigate ways of learning global structure without conditioning.


## GAN Preliminaries

Original formulation : minimax game between a generator $G : \mathcal{Z} \mapsto \mathcal{X}$ and a discriminator $D : \mathcal{X} \mapsto [0,1]$. <br>
$G$ has to minimize while $D$ has to maximize. That is to say, $D$ is trained to tell whether an input is fake or not, and $G$ to produce an output that will fool $D$.

`See formula in paper`

However, this methode is not performant for training, and instead, the Wasserstein-1 distance between generated and original data is chosen. <br>
This model is the *WGAN* and discriminator is trained to compute correctly Wasserstein-1 distance. <br>
A derivated model replaces *weight clipping* with a **gradient penalty**,  it is *WGAN-GP*.


## WaveGAN

### Audio vs Image

- Audio is more likely to show periodicity than images
- Images are more locally correlated

Filters with larger receptive fields are more relevant for audio signals, to capture periodicity. <br>
That's why WaveNet used *dilated convolutions*.

### WaveGAN architecture

DCGAN-like with some adjustments :
- *transposed convolution* in the *generator* is now a widening of the receptive field by 4 to upsample signal
- The *discriminator* sees a increase of stride by 4

All theses factors apply to each layers of course. An additional layer is added in the generative model to get 16384 samples. <br>
Which means a tiny bit more than a second of sound at a 16 kHz sample rate.

Steps summary :
1. Flatten 2D convolutions into 1D
2. Increase stride factor
3. Remove batch normalization
4. Use WGAN-GP strategy for training 

### Phase shuffle

Artifacts in audio can be interpreted as pitched noise, preventing the discriminator from discarding them. <br>
Fortunately, *phase* may be used to tell if it's consistent.

Using this, **phase shuffle** operation is set up with an hyperparameter $n$. <br>
It merely consists of a random shift of value $-n \leq i \leq n$ for each layer.

This increases the discriminator accuracy so that it requires phase consistency. <br>
Moreover, the gap due to the shift is filled by reflection ; it is depicted in the figure below, for $n = 1$.

![Phase Shuffle](https://gitgud.io/polochinoc/internship/raw/master/resources/notes/images/phase_shuffle.png)


## SpecGAN

Stakes
* Design a spectrogram modelisation suited to image-oriented GANs
* Design an pseudo-reversible spectrogram representation to translate it into raw audio

Procedure to generate spatial representation
- STFT with 16ms window size and 8ms stride which result in 128 freq bins
- Extract magnitude spectrum and apply logarithm to better suit human perception
- Normalize and center freq bins
- Clip spectra to 3 standard deviation and rescale to $[-1, 1]$

Procedure to get back to audio
- Invert all previous steps
- Apply Griffin-Lim algorithm


## Evaluation methodology

TODO : Complete this part

### Inception score

Usage of a pre-trained classifier, measuring diversity between generated samples and semantic. <br>
Is predicts pre-defined labels amongst $n$ different ones.

If $x$ and $y$ are labels, the inception score is defined by $exp(\mathbb{E}_x D_{KL}(P(y|x) || P(y)))$. <br>
It is maximized when the classifier is thoroughly confident and accurate about every prediction.

### Nearest neighbor

### Human judgment
