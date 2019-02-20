# WaveNet: A Generative Model for Raw Audio

## Introduction

*Can we use neural networks to generate coherent audio waveforms ?*
Constrained to high temporal resolution : at least 16000 samples per second for speech synthesis.
However, unlike images, it is a one-dimension data.
Usage of **autoregressive generative models** to address this problematic.
*WaveNet* is hereby described, and asserted better than all state-of-the-art TTS methods.
It is based on conditional probabilities.

## WaveNet

Generative model where *each audio sample depends on all the previous ones*.
If $x = \{x_1, ..., x_N\}$ is the waveform's raw data, then :
$p(x) = \Pi_{i=1}^N p(x_i | x_1, ..., x_{i-1})$
Model : stack of **convolutional layers**

Input : vector of values $\{x_1, ..., x_{i-1}\}$, processed by $i-1$ convolutional layers
Output : vector of probabilities for $x_i$ obtained using **softmax function**, to predict each audio sample.
This vector is then modified to maximize the **log-likelihood** of $x_t$ regarding the parameters.
These parameters being the possible values for $x_i$ represented by the vector of probabilities.

---

*Causal convolutions* imply a good ordering of the samples.
> Training time : parallel (all samples are known)
> Generating time : sequential
Issues to increase **receptive field**
- increase amount of layers
- increase filters size
Solution : *dilated convolutions*
It consists in skipping values with a given step, so that the filter size can be increased.
Moreover, the output size is kept identitical to the input size.
Enables to get large receptive fields while keeping a few layers.

---

