# -*- coding: utf-8 -*-

from colorama import Fore, Style

"""
Module to enhance your strings with colors and emphase
"""

def blue(string):
    '''Return colorized <string> in blue'''
    return ''.join([Fore.BLUE, str(string), Fore.RESET])

def cyan(string):
    '''Return colorized <string> in cyan'''
    return ''.join([Fore.CYAN, str(string), Fore.RESET])

def green(string):
    '''Return colorized <string> in green'''
    return ''.join([Fore.GREEN, str(string), Fore.RESET])

def black(string):
    '''Return colorized <string> in black'''
    return ''.join([Fore.BLACK, str(string), Fore.RESET])

def red(string):
    '''Return colorized <string> in red'''
    return ''.join([Fore.RED, str(string), Fore.RESET])

def yellow(string):
    '''Return colorized <string> in yellow'''
    return ''.join([Fore.YELLOW, str(string), Fore.RESET])

def magenta(string):
    '''Return colorized <string> in magenta'''
    return ''.join([Fore.MAGENTA, str(string), Fore.RESET])

def bright(string):
    '''Return brightened <string>, typically similar to bold font'''
    return ''.join([Style.BRIGHT, str(string), Style.RESET_ALL])

def dim(string):
    '''Return <string> with a sober grey-like font'''
    return ''.join([Style.DIM, str(string), Style.RESET_ALL])
