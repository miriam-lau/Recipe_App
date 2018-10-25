import sys


def get_debug_mode():
    debug_mode = False
    for arg in sys.argv:
        if arg == "--debugger":
            debug_mode = True
    return debug_mode
