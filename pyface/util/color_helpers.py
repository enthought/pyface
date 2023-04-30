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

from typing import cast, Iterable, NewType, Tuple, Type, Union

from typing_extensions import TypeGuard


#: A type representing a channel value between 0.0 and 1.0.
channel = NewType("channel", float)

#: A tuple of red, green, blue channels.
RGBTuple = Tuple[channel, channel, channel]

#: A tuple of red, green, blue, alpha channels.
RGBATuple = Tuple[channel, channel, channel, channel]


def channels_to_ints(
        channels: Iterable[channel],
        maximum: int = 255,
) -> Tuple[int, ...]:
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


def ints_to_channels(
        values: Iterable[int],
        maximum: int = 255,
) -> Tuple[channel, ...]:
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
    return tuple(channel(value / maximum) for value in values)


def relative_luminance(rgb: RGBTuple) -> float:
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


def is_dark(rgb: RGBTuple) -> bool:
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

    Returns
    -------
    is_dark : bool
        Whether the contrast against white is greater than the contrast against
        black.

    References
    ----------
    Understanding Web Contrast Accessibility Guidelines
    https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html#contrast-ratiodef
    """
    lumininance = relative_luminance(rgb)
    black_contrast = (lumininance + 0.05) / 0.05
    white_contrast = 1.05 / (lumininance + 0.05)
    return white_contrast > black_contrast


def int_to_color_tuple(value: int) -> RGBTuple:
    """Convert an int to a color, assuming a hex value of 0xRRGGBB

    Values outside 0, ..., 0xFFFFFF will raise a ValueError

    This is largely made available for backwards compatibility with old ETS
    color traits.

    Parameters
    ----------
    value : int
        Integer value of the form 0xRRGGBB

    Returns
    -------
    color : RGB tuple
        A tuple of RGB values from 0.0 to 1.0.
    """
    if 0 <= value <= 0xFFFFFF:
        return cast(RGBTuple, ints_to_channels(
            (value >> 16, (value >> 8) & 0xFF, value & 0xFF)
        ))
    else:
        raise ValueError(
            f"RGB integer value {value!r} must be between 0 and 0xFFFFFF"
        )


def sequence_to_rgba_tuple(value: Iterable[Union[float, int]]) -> RGBATuple:
    """Convert a sequence type to a tuple of RGB(A) value from 0.0 to 1.0

    This handles converson of 0, ..., 255 integer values and adding an alpha
    channel of 1.0, if needed.

    Parameters
    ----------
    value : sequence of ints or floats
        A sequence of length 3 or 4 of either integer values from 0 to 255, or
        floating point values from 0.0 to 1.0.

    Returns
    -------
    rgba_tuple : tuple of floats between 0.0 and 1.0
        A tuple of RGBA channel values, each value between 0.0 and 1.0,
        inclusive.

    Raises
    ------
    ValueError
        Raised if the sequence is of the wrong length or contains out-of-bounds
        values.
    """
    value = tuple(value)
    if _is_int_tuple(value):
        if all(0 <= x < 256 for x in value):
            channel_tuple = ints_to_channels(value)
        else:
            raise ValueError(
                f"Integer sequence values not in range 0 to 255: {value!r}"
            )
    else:
        channel_tuple = tuple(channel(x) for x in value)

    if _is_rgb_tuple(channel_tuple):
        rgba_tuple = channel_tuple + (channel(1.0),)
    elif _is_rgba_tuple(channel_tuple):
        rgba_tuple = channel_tuple
    else:
        raise ValueError("Sequence {value!r} must have length 3 or 4.")

    if all(0 <= x <= 1.0 for x in rgba_tuple):
        return rgba_tuple
    else:
        raise ValueError(
            f"Float sequence values not in range 0 to 1: {value!r}"
        )


def _is_int_tuple(
    value: Tuple[Union[float, int], ...]
) -> TypeGuard[Tuple[int, ...]]:
    int_types: Tuple[Type, ...]
    try:
        import numpy as np
        int_types = (int, np.integer)
    except ImportError:
        int_types = (int,)
    return all(isinstance(x, int_types) for x in value)


def _is_rgb_tuple(value: Tuple[channel, ...]) -> TypeGuard[RGBTuple]:
    return len(value) == 3


def _is_rgba_tuple(value: Tuple[channel, ...]) -> TypeGuard[RGBATuple]:
    return len(value) == 4
