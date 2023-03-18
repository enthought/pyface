# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Color conversion routines for the Qt toolkit.

This module provides a couple of utility methods to support the
pyface.color.Color class to_toolkit and from_toolkit methods.
"""

from pyface.qt.QtGui import QColor

from pyface.color import channels_to_ints, ints_to_channels


def toolkit_color_to_rgba(qcolor):
    """ Convert a QColor to an RGBA tuple.

    Parameters
    ----------
    qcolor : QColor
        A QColor object.

    Returns
    -------
    rgba_tuple : tuple
        A tuple of 4 floating point values between 0.0 and 1.0 inclusive.
    """
    values = (
        qcolor.red(),
        qcolor.green(),
        qcolor.blue(),
        qcolor.alpha(),
    )
    return ints_to_channels(values)


def rgba_to_toolkit_color(rgba):
    """ Convert an RGBA tuple to a QColor.

    Parameters
    ----------
    rgba_tuple : tuple
        A tuple of 4 floating point values between 0.0 and 1.0 inclusive.

    Returns
    -------
    qcolor : QColor
        A QColor object.
    """
    values = channels_to_ints(rgba)
    return QColor(*values)
