# Requirements

They are listed in *requirements.txt* file.

Just type `pip3 install -r requirements.txt` to get those.

If you wish to use a GPU, uncomment **magenta-gpu** and **tensorflow-gpu**, and comment **magenta** and **tensorflow**.

# Instructions

Put your audio files in *audio* directory (not necessary, it is merely cleaner).

Place your model files next to the python files.

There should be 3 model files for each model :
* <model_name>.data
* <model_name>.index
* <model_name>.meta

Just type <model_name> whenever using python scripts to designate 
your model.

## Pre-trained models

- WaveNet : [200000 iterations](http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar)
- GANSynth : [all instruments](https://storage.googleapis.com/magentadata/models/gansynth/all_instruments.zip), [acoustic only](https://storage.googleapis.com/magentadata/models/gansynth/acoustic_only.zip)

## Datasets

- NSynth : [test](http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz), [valid](http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-valid.jsonwav.tar.gz), [train](http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-train.jsonwav.tar.gz)

- MIDI : [J.S. Bach](http://www.jsbach.net/midi/index.html), [Classical Piano](www.piano-midi.de)