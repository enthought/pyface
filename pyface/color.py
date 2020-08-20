# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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

from traits.api import (
    HasStrictTraits, Property, Range, Tuple, cached_property
)


def channels_to_ints(channels, maximum=255):
    """ Convert an iterable of floating point channel values to integers.

    Values are rounded to the nearest integer, rather than truncated.

    Parameters
    ----------
    channels : iterable of float
        An iterable of channel values, each value between 0.0 and 1.0,
        inclusive.
    maximum : int
        The maximum value of the integer range.  Common values are 15,
        65535 or 255, which is the default.

    Returns
    -------
    values : tuple of int
        A tuple of values as integers between 0 and max, inclusive.
    """
    return tuple(int(round(channel * maximum)) for channel in channels)


def ints_to_channels(values, maximum=255):
    """ Convert an iterable of integers to floating point channel values.

    Parameters
    ----------
    values : tuple of int
        An iterable of values as integers between 0 and max, inclusive.
    maximum : int
        The maximum value of the integer range.  Common values are 15,
        65535 or 255, which is the default.

    Returns
    -------
    channels : iterable of float
        A tuple of channel values, each value between 0.0 and 1.0,
        inclusive.
    """
    return tuple(value / maximum for value in values)


#: A trait holding a single channel value.
Channel = Range(0.0, 1.0, value=1.0, channel=True)

#: A trait holding three channel values.
ChannelTuple = Tuple(Channel, Channel, Channel)

#: A trait holding four channel values.
AlphaChannelTuple = Tuple(Channel, Channel, Channel, Channel)


class Color(HasStrictTraits):
    """ A mutable specification of a color with alpha.

    This is a class designed to be used by user interface elements which
    need to color some or all of the interface element.  Each color has a
    number of different representations as channel tuples, each channel
    holding a value between 0.0 and 1.0, inclusive.  The standard red,
    green, blue and alpha channels are also provided as convenience
    properties.

    Methods are provided to convert to and from toolkit-specific color
    objects.

    Colors implement equality testing, but are not hashable as they are
    mutable, and so are not suitable for use as dictionary keys.  If you
    need a dictionary key, use an appropriate channel tuple from the
    object.
    """

    #: A tuple holding the red, green, blue, and alpha channels.
    rgba = AlphaChannelTuple()

    #: A tuple holding the red, green, and blue channels.
    rgb = Property(ChannelTuple(), depends_on='rgba')

    #: The red channel.
    red = Property(Channel, depends_on='rgba')

    #: The green channel.
    green = Property(Channel, depends_on='rgba')

    #: The blue channel.
    blue = Property(Channel, depends_on='rgba')

    #: The alpha channel.
    alpha = Property(Channel, depends_on='rgba')

    #: A tuple holding the hue, saturation, value, and alpha channels.
    hsva = Property(AlphaChannelTuple, depends_on='rgba')

    #: A tuple holding the hue, saturation, and value channels.
    hsv = Property(ChannelTuple, depends_on='rgb')

    #: A tuple holding the hue, lightness, saturation, and alpha channels.
    hlsa = Property(AlphaChannelTuple, depends_on='rgba')

    #: A tuple holding the hue, lightness, and saturation channels.
    hls = Property(ChannelTuple, depends_on='rgb')

    @classmethod
    def from_toolkit(cls, toolkit_color, **traits):
        """ Create a new Color object from a toolkit color object.

        Parameters
        ----------
        toolkit_color : toolkit object
            A toolkit color object, such as a Qt QColor or a Wx wx.Colour.
        **traits
            Any additional trait values to be passed as keyword arguments.
        """
        from pyface.toolkit import toolkit_object
        toolkit_color_to_rgba = toolkit_object('color:toolkit_color_to_rgba')
        rgba = toolkit_color_to_rgba(toolkit_color)
        return cls(rgba=rgba, **traits)

    def to_toolkit(self):
        """ Create a new toolkit color object from a Color object.

        Returns
        -------
        toolkit_color : toolkit object
            A toolkit color object, such as a Qt QColor or a Wx wx.Colour.
        """
        from pyface.toolkit import toolkit_object
        rgba_to_toolkit_color = toolkit_object('color:rgba_to_toolkit_color')
        return rgba_to_toolkit_color(self.rgba)

    def hex(self):
        """ Provide a hex representation of the Color object.

        Note that because the hex value is restricted to 0-255 integer values
        for each channel, the representation is not exact.

        Returns
        -------
        hex : str
            A hex string in standard ``#RRGGBBAA`` format that represents
            the color.
        """
        values = channels_to_ints(self.rgba)
        return "#{:02X}{:02X}{:02X}{:02X}".format(*values)

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.rgba == other.rgba
        return NotImplemented

    def __str__(self):
        return "({:0.5}, {:0.5}, {:0.5}, {:0.5})".format(*self.rgba)

    def __repr__(self):
        return "{}(rgba={!r})".format(self.__class__.__name__, self.rgba)

    def _get_red(self):
        return self.rgba[0]

    def _set_red(self, value):
        r, g, b, a = self.rgba
        self.rgba = (value, g, b, a)

    def _get_green(self):
        return self.rgba[1]

    def _set_green(self, value):
        r, g, b, a = self.rgba
        self.rgba = (r, value, b, a)

    def _get_blue(self):
        return self.rgba[2]

    def _set_blue(self, value):
        r, g, b, a = self.rgba
        self.rgba = (r, g, value, a)

    def _get_alpha(self):
        return self.rgba[3]

    def _set_alpha(self, value):
        r, g, b, a = self.rgba
        self.rgba = (r, g, b, value)

    @cached_property
    def _get_rgb(self):
        return self.rgba[:-1]

    def _set_rgb(self, value):
        r, g, b = value
        self.rgba = (r, g, b, self.rgba[3])

    @cached_property
    def _get_hsva(self):
        r, g, b, a = self.rgba
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h, s, v, a)

    def _set_hsva(self, value):
        h, s, v, a = value
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.rgba = (r, g, b, a)

    @cached_property
    def _get_hsv(self):
        r, g, b = self.rgb
        return colorsys.rgb_to_hsv(r, g, b)

    def _set_hsv(self, value):
        h, s, v = value
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        self.rgb = (r, g, b)

    @cached_property
    def _get_hlsa(self):
        r, g, b, a = self.rgba
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return (h, l, s, a)

    def _set_hlsa(self, value):
        h, l, s, a = value
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        self.rgba = (r, g, b, a)

    @cached_property
    def _get_hls(self):
        r, g, b = self.rgb
        return colorsys.rgb_to_hls(r, g, b)

    def _set_hls(self, value):
        h, l, s = value
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        self.rgb = (r, g, b)
