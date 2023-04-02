# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Color conversion routines for the null toolkit.

This module provides a couple of utility methods to support the
pyface.color.Color class to_toolkit and from_toolkit methods.

For definiteness, the null toolkit uses tuples of RGBA values from 0 to 255
to represent colors.
"""

from pyface.color import channels_to_ints, ints_to_channels


def toolkit_color_to_rgba(color):
    """ Convert a hex tuple to an RGBA tuple.

    Parameters
    ----------
    color : tuple
        A tuple of integer values from 0 to 255 inclusive.

    Returns
    -------
    rgba : tuple
        A tuple of 4 floating point values between 0.0 and 1.0 inclusive.
    """
    return ints_to_channels(color)


def rgba_to_toolkit_color(rgba):
    """ Convert an RGBA tuple to a hex tuple.

    Parameters
    ----------
    color : tuple
        A tuple of integer values from 0 to 255 inclusive.

    Returns
    -------
    rgba : tuple
        A tuple of 4 floating point values between 0.0 and 1.0 inclusive.
    """
    return channels_to_ints(rgba)
