import sys
from .qt import *


def get_argv_or_dialog():
    if len(sys.argv) > 1:
        return sys.argv[1:]
    else:
        filenames, _ = QFileDialog().getOpenFileNames()
        return filenames
