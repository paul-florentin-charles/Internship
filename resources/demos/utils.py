## Utils ##

def get_extension(_file):
    '''
    Takes a string <_file>
    Returns string stripped of the characters before its last point (included), if it has any. Otherwise, returns the same string
    '''
    return _file[_file.rfind('.') + 1:]

def without_extension(_file):
    '''
    Takes a string <_file>
    Returns string stripped of the characters after its last point (included), if it has any. Otherwise, returns the same string
    '''
    return _file[:_file.rfind('.')]
