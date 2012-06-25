# Copyright 2012 Philip Chimento

"""
Sound the system bell, null toolkit implementation.
Tries to print the \\a character (BEL, 007, ^G) to the terminal.
"""


def beep():
    """Sound the system bell."""
    # This probably won't work, but it's worth a shot.
    print('\a')
