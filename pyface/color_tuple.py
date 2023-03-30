# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Color classes and corresponding trait types for Pyface.

The base Color class holds red, green, blue and alpha channel values as
a tuple of normalized values from 0.0 to 1.0.  Various property traits
pull out the individual channel values and supply values for the HSV
and HSL colour spaces (with and without alpha).

The ``from_toolkit`` and ``to_toolkit`` methods allow conversion to and
from native toolkit color objects.
"""

import colorsys
from typing import NamedTuple, Tuple, TYPE_CHECKING

from pyface.util.color_helpers import (
    channel, channels_to_ints, is_dark, RGBTuple
)
from pyface.util.color_parser import parse_text

if TYPE_CHECKING:
    from .color import Color


class ColorTuple(NamedTuple):
    """An immutable specification of a color with alpha.

    This is a namedtuple designed to be used by user interface elements which
    need to color some or all of the interface element.  Each color has a
    number of different representations as channel tuples, each channel
    holding a value between 0.0 and 1.0, inclusive.  The standard red,
    green, blue and alpha channels are also provided as convenience
    properties.

    Methods are provided to convert to and from toolkit-specific color
    objects.

    ColorTuples can be tested for equality and are hashable, just as with all
    namedtuples, and so are suitable for use as dictionary keys.
    """

    red: channel = channel(1.0)

    green: channel = channel(1.0)

    blue: channel = channel(1.0)

    alpha: channel = channel(1.0)

    @classmethod
    def from_str(cls, text: str):
        """ Create a new ColorTuple from a string.

        Parameters
        ----------
        text : str
            A string holding the representation of the color.  This can be:

            - a color name, including all CSS color names, plus any additional
              names found in pyface.color.color_table.  The names are
              normalized to lower case and stripped of whitespace, hyphens and
              underscores.

            - a hex representation of the color in the form '#RGB', '#RGBA',
              '#RRGGBB', '#RRGGBBAA', '#RRRRGGGGBBBB', or '#RRRRGGGGBBBBAAAA'.

        Raises
        ------
        ColorParseError
            If the string cannot be converted to a valid color.
        """
        space, channels = parse_text(text)
        return cls(*channels)

    @classmethod
    def from_color(cls, color: "Color") -> "ColorTuple":
        """ Create a new ColorTuple from a Color object.

        Parameters
        ----------
        color : Color
            A Color object.
        """
        return cls(*color.rgba)

    @classmethod
    def from_toolkit(cls, toolkit_color) -> "ColorTuple":
        """ Create a new RGBAColorTuple from a toolkit color object.

        Parameters
        ----------
        toolkit_color : toolkit object
            A toolkit color object, such as a Qt QColor or a Wx wx.Colour.
        **traits
            Any additional trait values to be passed as keyword arguments.
        """
        from pyface.toolkit import toolkit_object
        toolkit_color_to_rgba = toolkit_object('color:toolkit_color_to_rgba')
        return cls(*toolkit_color_to_rgba(toolkit_color))

    def to_toolkit(self):
        """ Create a new toolkit color object from a Color object.

        Returns
        -------
        toolkit_color : toolkit object
            A toolkit color object, such as a Qt QColor or a Wx wx.Colour.
        """
        from pyface.toolkit import toolkit_object
        rgba_to_toolkit_color = toolkit_object('color:rgba_to_toolkit_color')
        return rgba_to_toolkit_color(self)

    def hex(self) -> str:
        """ Provide a hex representation of the Color object.

        Note that because the hex value is restricted to 0-255 integer values
        for each channel, the representation is not exact.

        Returns
        -------
        hex : str
            A hex string in standard ``#RRGGBBAA`` format that represents
            the color.
        """
        values = channels_to_ints(self)
        return "#{:02X}{:02X}{:02X}{:02X}".format(*values)

    def __str__(self) -> str:
        return "({:0.5}, {:0.5}, {:0.5}, {:0.5})".format(*self)

    @property
    def rgb(self) -> RGBTuple:
        return self[:3]

    @property
    def hsva(self) -> Tuple[channel, channel, channel, channel]:
        r, g, b, a = self
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h, s, v, a)

    @property
    def hsv(self) -> Tuple[channel, channel, channel]:
        r, g, b, a = self
        return colorsys.rgb_to_hsv(r, g, b)

    @property
    def hlsa(self) -> Tuple[channel, channel, channel, channel]:
        r, g, b, a = self
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h, l, s, a)

    @property
    def hls(self) -> Tuple[channel, channel, channel]:
        r, g, b, a = self
        return colorsys.rgb_to_hls(r, g, b)

    @property
    def is_dark(self) -> bool:
        return is_dark(self)
