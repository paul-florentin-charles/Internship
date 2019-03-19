# -*- coding: utf-8 -*-

from src.colors import *

def usage(pname, required_args = [], optional_args = []):
    raise SystemExit(''.join([bright('Usage:'), magenta_fg(' python3 '), cyan_fg(pname), ' ', ' '.join(required_args), ' ', ' '.join([''.join(['[', arg, ']']) for arg in optional_args])]))


#TODO: use *fleep* library to check wether audio file or not
def is_audio_file(fpath):
    pass
