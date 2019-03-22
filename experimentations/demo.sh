if [[ $0 != "demo.sh" ]] && [[ $0 != "./demo.sh" ]]
then
    echo "Execute script from its directory"
    exit 1
fi

echothief_url=http://www.echothief.com/wp-content/uploads/2016/06/EchoThiefImpulseResponseLibrary.zip
nsynthtest_url=http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz

# Getting EchoThief
echo "Getting EchoThief dataset of impulse responses"
curl -O $echothief_url
unzip EchoThiefImpulseResponseLibrary.zip
rm -rf EchoThiefImpulseResponseLibrary.zip __MACOSX
mv EchoThiefImpulseResponseLibrary echo-thief

# Getting filtered version of NSynth
echo -e "\nGetting NSynth test dataset"
curl -O $nsynthtest_url
tar -xvf nsynth-test.jsonwav.tar.gz
rm -rf nsynth-test.jsonwav.tar.gz

# Creating dataset (this will be long...)
echo -e "\nConvolving NSynth notes with EchoThief impulse responses"
echo "Feel free to interrupt process, information are saved progressively"
mkdir nsynth-echo-thief
./main.py echo-thief nsynth-test nsynth-echo-thief

