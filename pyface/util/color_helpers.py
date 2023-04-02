# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Routines supporting color computations

Most of what is needed is provided by Python's builtin colorsys module,
but we need a few additional routines for things that are not covered by
that code.
"""


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


def relative_luminance(rgb):
    """ The relative luminance of the color.

    This value is the critical value when comparing colors for contrast when
    displayed next to each other, in particular for readability of text.

    Parameters
    ----------
    rgb : tuple of red, green, blue values
        A tuple of values representing red, green and blue components of
        the color, as values from 0.0 to 1.0.

    Returns
    -------
    luminance : float
        The relative luminance of the color.

    References
    ----------
    Web Contrast Accessibility Guidelines
    https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
    """
    gamma_corrected = [
        x/12.92 if x <= 0.03928 else ((x + 0.055)/1.055)**2.4
        for x in rgb
    ]
    luminance = (
        0.2126 * gamma_corrected[0]
        + 0.7152 * gamma_corrected[1]
        + 0.0722 * gamma_corrected[2]
    )
    return luminance


def is_dark(rgb):
    """ Is the color dark to human perception?

    A color is dark if white contasts better with it according to the WC3
    definition of contrast ratio.  This is allows GUI code to choose either
    black or white as a contrasting color for things like text on a colored
    background.

    Parameters
    ----------
    rgb : tuple of red, green, blue values
        A tuple of values representing red, green and blue components of
        the color, as values from 0.0 to 1.0.

    References
    ----------
    Understanding Web Contrast Accessibility Guidelines
    https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html#contrast-ratiodef
    """
    lumininance = relative_luminance(rgb)
    black_contrast = (lumininance + 0.05) / 0.05
    white_contrast = 1.05 / (lumininance + 0.05)
    return white_contrast > black_contrast
