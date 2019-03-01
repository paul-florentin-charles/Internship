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

### Dilated causal convolutions

*Causal convolutions* imply a good ordering of the samples.
- Training time : parallel (all samples are known)
- Generating time : sequential

Issues to increase **receptive field**
- increase amount of layers
- increase filters size

Solution : *dilated convolutions*

It consists in skipping values with a given step, so that the filter size can be increased.

Moreover, the output size is kept identitical to the input size.

Enables to get large receptive fields while keeping a few layers.

### Softmax distributions

*Softmax* is to be applied on large vectors (65,536 for a bit-depth of 16).

Therefore we apply a **$\mu$-law** first ($\mu = 255$), and quantize it to 256 values.

This non-linear function induces a more natural reconstruction, especially for speech.

It reduces the dynamic range with its logarithm, allowing fine details to be perceived.

### Gated activation units

Non-linear formula that works better than *ReLU*.

$z = tanh(W_{f,k} * x) \odot \sigma (W_{g,k} * x)$

With *W* representing **convolutional filters**, and $\odot$ a element-wise multiplication.

Two different activation functions are combined after convolution is applied to the raw data.

### Residual and skip connections

They speed up the process. 

Below is a figure extracted from the paper, that depicts WaveNet's architecture.

![WaveNet Architecture](https://gitgud.io/polochinoc/internship/raw/master/resources/notes/images/wavenet.png)

#### Some comments

- *1x1* denotes a 1-D convolution with a filter of size 1
- the number of layers is the number of convolution filters
- **Residual** means we add the original input $x$ to $z$ ($x$ processed through *gated activation unit*)

### Conditional WaveNets

$p(x | __h__) = \Pi_{i=1}^N p(x_i | x_1, ..., x_{i-1}, __h__)$

Adding a further condition can be interesting to add extra information such as the speaker's identity.

This condition can either be global and apply to all probabilities, or local and therefore be a vector of conditions.

In the case of TTS, it is text information.