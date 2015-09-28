# Copyright 2012 Philip Chimento

"""Sound the system bell, Qt implementation."""

from pyface.qt import QtWidgets


def beep():
    """Sound the system bell."""
    QtWidgets.QApplication.beep()
