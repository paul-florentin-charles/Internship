# -*- coding: utf-8 -*-

from colorama import Fore, Style

"""
Module to enhance your strings with colors and emphase
"""

def _blue_(string):
    '''Return colorized <string> in blue'''
    return ''.join([Fore.BLUE, str(string), Fore.RESET])

def _cyan_(string):
    '''Return colorized <string> in cyan'''
    return ''.join([Fore.CYAN, str(string), Fore.RESET])

def _green_(string):
    '''Return colorized <string> in green'''
    return ''.join([Fore.GREEN, str(string), Fore.RESET])

def _black_(string):
    '''Return colorized <string> in black'''
    return ''.join([Fore.BLACK, str(string), Fore.RESET])

def _red_(string):
    '''Return colorized <string> in red'''
    return ''.join([Fore.RED, str(string), Fore.RESET])

def _yellow_(string):
    '''Return colorized <string> in yellow'''
    return ''.join([Fore.YELLOW, str(string), Fore.RESET])

def _magenta_(string):
    '''Return colorized <string> in magenta'''
    return ''.join([Fore.MAGENTA, str(string), Fore.RESET])

def _bright_(string):
    '''Return brightened <string>, typically similar to bold font'''
    return ''.join([Style.BRIGHT, str(string), Style.RESET_ALL])

def _dim_(string):
    '''Return <string> with a sober grey-like font'''
    return ''.join([Style.DIM, str(string), Style.RESET_ALL])
