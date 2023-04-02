# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Color conversion routines for the wx toolkit.

This module provides a couple of utility methods to support the
pyface.color.Color class to_toolkit and from_toolkit methods.
"""


import wx

from pyface.color import channels_to_ints, ints_to_channels


def toolkit_color_to_rgba(wx_colour):
    """ Convert a wx.Colour to an RGBA tuple.

    Parameters
    ----------
    wx_color : wx.Colour
        A wx.Colour object.

    Returns
    -------
    rgba : tuple
        A tuple of 4 floating point values between 0.0 and 1.0 inclusive.
    """
    values = (
        wx_colour.Red(),
        wx_colour.Green(),
        wx_colour.Blue(),
        wx_colour.Alpha(),
    )
    return ints_to_channels(values)


def rgba_to_toolkit_color(rgba):
    """ Convert an RGBA tuple to a wx.Colour.

    Parameters
    ----------
    rgba : tuple
        A tuple of 4 floating point values between 0.0 and 1.0 inclusive.

    Returns
    -------
    wx_color : wx.Colour
        A wx.Colour object.
    """
    values = channels_to_ints(rgba)
    return wx.Colour(*values)
