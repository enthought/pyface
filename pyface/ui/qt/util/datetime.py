# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Utility functions for handling Qt dates and times. """

from pyface.qt import is_pyqt
from pyface.qt.QtCore import QTime


def qtime_to_pytime(qtime):
    """ Convert a QTime to a Python datetime.time

    This is needed to paper over the differences between PyQt and PySide.

    Parameters
    ----------
    qtime : QTime
        The Qt QTime to convert

    Returns
    -------
    pytime : datetime.time
        The corresponding datetime.time.
    """
    if is_pyqt:
        return qtime.toPyTime()
    else:
        return qtime.toPython()


def pytime_to_qtime(pytime):
    """ Convert a Python datetime.time to a QTime

    This is a convenience function to construct a qtime from a Python time.
    This loses any :attr:`fold` information in the Python time.

    Parameters
    ----------
    pytime : datetime.time
        The datetime.time to convert

    Returns
    -------
    qtime : QTime
        The corresponding Qt QTime.
    """
    return QTime(
        pytime.hour,
        pytime.minute,
        pytime.second,
        pytime.microsecond // 1000
    )
