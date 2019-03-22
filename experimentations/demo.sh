#TODO: Improve and clean up this messy script

if [[ $0 != "demo.sh" ]] && [[ $0 != "./demo.sh" ]]
then
    echo "Execute script from its directory"
    exit 1
fi

fx_url=http://www.echothief.com/wp-content/uploads/2016/06/EchoThiefImpulseResponseLibrary.zip
notes_url=http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz

fx_fname=EchoThiefImpulseResponseLibrary.zip
notes_fname=nsynth-test.jsonwav.tar.gz

# Getting EchoThief
if [ ! -d "echo-thief" ]
then
    echo "Getting EchoThief dataset of impulse responses"
    curl -O $fx_url
    unzip $fx_fname -d echo-thief
    rm -rf $fx_fname __MACOSX
#    mv EchoThiefImpulseResponseLibrary echo-thief
fi
    
# Getting filtered version of NSynth
if [ ! -d "nsynth-test" ]
then
    echo -e "\nGetting NSynth test dataset"
    curl -O $notes_url
    tar -xvf $notes_fname
    rm -rf $notes_fname
fi

# Creating dataset (this will be long...)
if [ ! -d "nsynth-echo-thief" ]
then
    echo -e "\nConvolving NSynth notes with EchoThief impulse responses"
    echo "Feel free to interrupt process, information are saved progressively"
    mkdir nsynth-echo-thief
    ./main.py echo-thief nsynth-test nsynth-echo-thief
else
    echo -e "\nYou already have launched demo, please remove nsynth-echo-thief folder"
fi
