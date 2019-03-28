#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datagen.utils import _load, _export, _read, __list_audio_files
from datagen.misc import usage, mkrdir
from datagen.fx import _apply_fxs
import datagen.path as pth
import parser._json as jsn, parser._toml as tml
from neuralnet.utils import retrieve_data
#import neuralnet.model as nnmodel

import sys

def main(dry_dpath, ir_dpath, output_dir):
    # Dataset generation

    save_steps, json_fname = tml.value('meta', 'save_steps'), tml.value('meta', 'json_fname')

    impulse_responses = _load(ir_dpath)

    pth.__create_file(json_fname)
    
    info = dict()
        
    for idx, dryfpath in enumerate(__list_audio_files(dry_dpath)):
        wet_signals = _apply_fxs(_read(dryfpath), impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        _export(wet_signals, dpath)

        jsn._write(info, str(dryfpath), str(dpath))
        
        if (idx + 1) % save_steps == 0:
            jsn._dump(json_fname, info)

    jsn._dump(json_fname, info)

    # Model training

    data, labels = retrieve_data()

    """
    model = nnmodel._init()
    nnmodel._compile(model)
    nnmodel._train(model, data, labels)
    print(nnmodel._evaluate(model, data, labels)
    """

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise SystemExit(usage(__file__.replace('./', ''), ['path/to/dry/signals/dir', 'path/to/impulse/responses/dir', 'path/to/output/dir']))
    
    main(*sys.argv[1:])
