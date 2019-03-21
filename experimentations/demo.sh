if [[ $0 != "demo.sh" ]] && [[ $0 != "./demo.sh" ]]
then
    echo "Execute script from it directory"
    exit 1
fi

# Getting EchoThief
curl -O http://www.echothief.com/wp-content/uploads/2016/06/EchoThiefImpulseResponseLibrary.zip
unzip EchoThiefImpulseResponseLibrary.zip
rm -rf EchoThiefImpulseResponseLibrary.zip __MACOSX
mv EchoThiefImpulseResponseLibrary echo-thief

# Getting filtered version of NSynth
curl -O http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz
tar -xvf nsynth-test.jsonwav.tar.gz
rm -rf nsynth-test.jsonwav.tar.gz

# Creating dataset (this will be long...)
mkdir nsynth-echo-thief
./main.py echo-thief nsynth-test nsynth-echo-thief
