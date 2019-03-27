# TODO: add colors or convert to python script

if [[ $0 != "demo.sh" ]] && [[ $0 != "./demo.sh" ]]
then
    echo "Execute script from its directory"
    exit 1
fi

base_url=https://raw.githubusercontent.com/polochinoc/various-audio-datasets/master/

fx_base_url=$base_url"ir_dataset_"
notes_base_url=$base_url"note_dataset_"

fx_extension=".zip"
notes_extension=".tar.gz"

# Initializing URLs and directory names
if [[ $md == "long" ]]
then
    fx_url=$fx_base_url"medium"$fx_extension
    notes_url=$notes_base_url"big"$notes_extension
elif [[ $md == "slow" ]]
then
    fx_url=$fx_base_url"small"$fx_extension
    notes_url=$notes_base_url"medium"$notes_extension
elif [[ $md == "fast" ]]
then
    fx_url=$fx_base_url"small"$fx_extension
    notes_url=$notes_base_url"small"$notes_extension
elif [[ $md == "quick" ]]
then
    fx_url=$fx_base_url"tiny"$fx_extension
    notes_url=$notes_base_url"small"$notes_extension
else
    fx_url=$fx_base_url"tiny"$fx_extension
    notes_url=$notes_base_url"tiny"$notes_extension
fi

fx_fname=${fx_url##*/}
notes_fname=${notes_url##*/}

fx_dname="fx"
dry_dname="dry"
wet_dname="wet"

# Getting IRs
if [ ! -d $fx_dname ]
then
    echo "Retrieving dataset of fxs"
    curl -O $fx_url
    unzip $fx_fname -d $fx_dname
    rm -rf $fx_fname
fi
    
# Getting Dry Signals
if [ ! -d $dry_dname ]
then
    echo -e "\nRetrieving dataset of dry signals"
    curl -O $notes_url
    mkdir -p $dry_dname
    tar -xvf $notes_fname -C $dry_dname --strip-components=1
    rm -rf $notes_fname
fi

# Creating dataset of Wet Signals
if [ ! -d $wet_dname ]
then
    echo -e "\nGenerating dataset of wet signals"
    echo "Feel free to interrupt process, information are saved progressively"
    mkdir -p $wet_dname
    ./main.py $fx_dname $dry_dname $wet_dname
    echo "Done"
else
    echo "You already have launched demo, please remove {"$wet_dname"} folder to relaunch demo, or even do {make cleanall} if you wish to launch another demo"
fi
