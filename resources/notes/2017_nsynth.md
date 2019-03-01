# Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders


## Introduction

Audio synthesis based on WaveNet, adapted to be an autoencoder. <br>
Therefore it needn't any external conditioning since it is biased using a temporal encoder.

For the purpose of the training, a big dataset has been set up : *NSynth*. <br>
It consists of ~300k 4-second notes, sampled at 16 kHz from 1k instruments.

WaveNet works for short signal (~0.5s), and relies on conditioning for longer signals. <br>
Here, we have a WaveNet-like encoder that produces **embeddings** applied as biases on a WaveNet decoder.

Since embeddings can potentially be as long as wanted (only limited by complexity), the reconstructed signal can be longer. <br>
WaveNet is evaluated over a baseline model trained on spectrograms.


## Models

### WaveNet Autoencoder

Probabilistic model to generate raw audio, sample by sample. <br>
Handy approach to reach consistent long-term structures as said before, but also to combine encodings (mix, crossfade, etc.)

Check `2016_wavenet.md` for the mechanism of WaveNet.

Instead of using an external __h__ set by the user, which is a hyperparameter such as the speaker position (L or R), if it's in stereo. <br>
The WaveNet-style encoder produces an embedding $Z = f(x)$ from the raw audio $x$. <br>
This embedding is fed to the WaveNet decoder, used as a conditional probability. <br>
It could be ignored by the decoder which would then act as a standard WaveNet. <br>
However, since it is a strong information, it affects the model.

The embedding is inferred from the raw audio and completed thanks to interpolation. <br>
It is a 2-dimensional array : **(time\_steps, n\_channels).** <br>
**Stride of the pooling** affects time resolution, while dimension depends on the convolution final number of channels. <br>
All the notes embeddings can be regrouped in a 3-d array : (batch\_size, time\_steps, n\_channels).

To be processed by the decoder, embeddings are upsampled to the original audio rate, with *nearest neighbour interpolation*. <br>
Embeddings are also concatenated with one-hot pitch encoding to add further information, notably to keep pitch coherent. <br>
Then each layer is biased using **different linear projections of the embeddings**. <br>
Apart from this, decoder works like *WaveNet* decoder described in `2016_wavenet.md`.

Below is a figure showcasing the autoencoder.

![WaveNet Autoencoder](https://gitgud.io/polochinoc/internship/raw/master/resources/notes/images/nsynth.png)

### Baseline Autoencoder

Made of two CNN, one to encode signal from a spectrogram and through 10 layers. <br>
The other to decode spectrogram through 10 layers as well with biases defined by the encoder concatenated to a pitch encoding. <br>
The encoder's embedding is set to match the total number of convolutional filters of the decoder, thanks to a fully connected layer at the end.

Raw audio has not been chosen since its learning rate through MSE error proved itself slow. <br>
On the other hand, spectral representation using FFT components worked better, but didn't have expected sounding quality. <br>
Notably working on the log amplitude, normalize betwee 0 and 1.

Phase is also a used feature. Firstly independently estimated using instantaneous frequency, but then reconstructed from the magnitude. <br>
Used heuristic is a *weighted MSE*, that gives more importance to lower frequencies for learning. <br>
It gives better phase restitution for the fundamentals.

Underneath is a figure showcasing the baseline.

![Baseline Autoencoder](https://gitgud.io/polochinoc/internship/raw/master/resources/notes/images/baseline_autoencoder.png)

### Training

**Stochastic gradient descent** with and **Adam optimizer**. <br>
Learning rate is constant for baseline but decreasing for WaveNet autoencoder.


## NSynth Dataset

Consists solely of musical notes (~300k), with the full range of pitches in a piano (88), and with 5 different values of velocity. <br>
Each note is held for the first 3 seconds, and released for 1 second.

Furthermore, every note is annotated accorting to 3 criteria :
* Source : acoustic, electronic or synthetic
* Family : bass, brass, flute, guitar, keyboad, mallet, organ, reed, string, synth lead or vocal
* Qualities : bright, dark, distortion, fast decay, lon release, multiphonic, NL envelope, percussive, reverb and tempo-synced


## Evaluation

3 tasks :
- note reconstruction
- instrument interpolation
- pitch interpolation

Used representation : Constant Q Transform. <br>
--> Insensitive to shift in the fundamental frequency. <br>
--> Displays phase information

It remains a visual representation, and two lookalike spectrums don't necessarily mean the sounds are similar. <br>
But it has more information, especially about the phase.

Intensity of colours depends on the log magnitude, while colour itself depends on the phase derivative **(instantaneous frequency)**. <br>
If a harmony keeps a consistent frequency, the dephasing between harmonics will remain constant, therefore a null derivative. <br>
In the graphic, it is translated by a continuous horizontal line of constant colour.

*Rainbowgram*

$\Delta \phi = (f_{bin} - f_{harm}) \frac{hopsize}{samplerate}$

This constant phase shift is at the origin of the phase modulation that produces "rainbows". <br>
$f\_{bin}$ is the closest discretized frequency, and $f\_{harm}$ is the actual frequency.
 
### Reconstruction

Check the paper for some detailed interpretation of some results.

