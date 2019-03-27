#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datagen.utils import _load, _export, _read, __list_audio_files
from datagen.misc import usage, mkrdir
from datagen.fx import _apply_fxs
import parser._json as pjsn
import parser._toml as ptml
from neuralnet.utils import retrieve_data
#import neuralnet.model as nnmodel

import sys

def main():
    argc = len(sys.argv)

    if argc < 3:
        raise SystemExit(usage(__file__.replace('./', ''), ['path/to/impulse/responses/dir', 'path/to/dry/signals/dir'], ['path/to/output/dir']))

    # Dataset generation
    
    output_dir = sys.argv[3] if argc > 3 else mkrdir()

    impulse_responses = _load(sys.argv[1])

    save_steps, json_fname = ptml.value('meta', 'save_steps'), ptml.value('meta', 'json_fname')

    open(json_fname, 'w').close()
    
    info = dict()
        
    for idx, dryfpath in enumerate(__list_audio_files(sys.argv[2])):
        wet_signals = _apply_fxs(_read(dryfpath), impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        _export(wet_signals, dpath)

        pjsn._write(info, str(dryfpath), str(dpath))
        
        if (idx + 1) % save_steps == 0:
            pjsn._dump(json_fname, info)

    pjsn._dump(json_fname, info)

    # Model training

    data, labels = retrieve_data()

    """
    model = nnmodel._init()
    nnmodel._compile(model)
    nnmodel._train(model, data, labels)
    print(nnmodel._evaluate(model, data, labels)
    """

if __name__ == '__main__':
    main()
