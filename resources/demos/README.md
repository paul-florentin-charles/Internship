# Requirements

They are listed in *requirements.txt* file.

Just type `pip3 install -r requirements` to get those.

If you wish to use a GPU, uncomment **magenta-gpu** and **tensorflow-gpu**, and comment **magenta** and **tensorflow**.

# Instructions

Put your audio files in *audio* directory (not necessary, it is 
merely cleaner).

Place your model files next to the python files ; you can grab one that is pre-trained at [wavenet-cpkt](http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar).

There should be 3 model files for each model :
* <model_name>.data
* <model_name>.index
* <model_name>.meta

Just type <model_name> whenever using python scripts to designate 
your model.
