__config__ = {
    "url": None,

}

from .mod import BianceDataMode


def load_mod():
    return BianceDataMode()