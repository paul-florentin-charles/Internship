#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.datagen.utils import _load, _export, _read, __list_audio_files
from src.utils.tools import usage, mkrdir
import src.utils.logger as log
from src.datagen.fx import _apply_fxs
import src.utils.path as pth
import src.parser.json as jsn, src.parser.toml as tml
from src.neuralnet.utils import retrieve_data
#import src.neuralnet.model as nnmodel

import sys

def main(dry_dpath, ir_dpath, output_dir):
    # Dataset generation

    if not pth.__exists(output_dir):
        pth.__make_dir(output_dir)

    save_steps, json_fname = tml.value('meta', 'save_steps'), tml.value('meta', 'json_fname')

    impulse_responses = _load(ir_dpath)

    pth.__create_file(json_fname)
    
    info = dict()

    log.info('Generating dataset of wet samples')
        
    for idx, dryfpath in enumerate(__list_audio_files(dry_dpath)):
        wet_signals = _apply_fxs(_read(dryfpath), impulse_responses)
        dpath = mkrdir(output_dir, prefix=''.join([str(idx), '_']))
        _export(wet_signals, dpath)

        jsn._write(info, str(dryfpath), str(dpath))
        
        if (idx + 1) % save_steps == 0:
            jsn._dump(json_fname, info)

    jsn._dump(json_fname, info)

    # Model training

    log.info('Shaping data to feed them to the model')

    data, labels = retrieve_data()

    log.info('Training the model')

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
