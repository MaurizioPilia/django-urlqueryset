from .urlqueryset import *

VERSION = (0, 1, 0)

__version__ = '.'.join([str(n) for n in VERSION])


def get_version():
    return __version__

