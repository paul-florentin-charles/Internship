#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datagen.path as pth
import parser._toml as tml
from main import main

from subprocess import call
from shutil import unpack_archive

    
def demo():
    # Scraping data from URLs
    
    base_url = tml.value('demo', 'datasets_url')

    note_url = ''.join([base_url, 'note_dataset_', tml.value('demo', 'size'), '.tar.gz'])
    fx_url = ''.join([base_url, 'ir_dataset_', tml.value('demo', 'size'), '.zip'])

    call(['curl', '-O', note_url, '-O', fx_url])

    # Extracting data

    dnames = tml.value('demo', 'dnames')

    note_fname, fx_fname = map(pth.__file_name, (note_url, fx_url))

    unpack_archive(note_fname, dnames[0])
    unpack_archive(fx_fname, dnames[1])
    
    pth.__remove_file(note_fname)
    pth.__remove_file(fx_fname)

    # Execute main script

    pth.__make_dir(dnames[2])

    main(*dnames)


if __name__ == '__main__':
    if __file__.replace('./', '') != "demo.py":
        raise SystemExit("Please execute script from its directory")
    
    demo()
