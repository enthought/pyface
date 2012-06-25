# Copyright 2012 Philip Chimento

"""Sound the system bell, Qt implementation."""

from pyface.qt import QtGui


def beep():
    """Sound the system bell."""
    QtGui.QApplication.beep()
