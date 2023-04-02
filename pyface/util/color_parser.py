# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Color string parser for Pyface.

The ``parse_text`` function allows the creation of Color objects from
CSS-style strings, including all the CSS names colours or hex strings starting
with "#".  If there is no match, a ColorParseError is raised.

A dictionary of named colours is available as the color_table module-level
dictionary.  This dictionary holds all CSS colour names, plus a number of
other names such as "transparent".

Additionally, two utility functions ``channels_to_ints`` and
``ints_to_channels`` are provided to assist in converting between floating
point and integer values.
"""

import re

from .color_helpers import ints_to_channels


#: A dictionary mapping known color names to rgba tuples.
color_table = {
    "aliceblue": (0.941, 0.973, 1.000, 1.0),
    "antiquewhite": (0.980, 0.922, 0.843, 1.0),
    "aqua": (0.000, 1.000, 1.000, 1.0),
    "aquamarine": (0.498, 1.000, 0.831, 1.0),
    "azure": (0.941, 1.000, 1.000, 1.0),
    "beige": (0.961, 0.961, 0.863, 1.0),
    "bisque": (1.000, 0.894, 0.769, 1.0),
    "black": (0.000, 0.000, 0.000, 1.0),
    "blanchedalmond": (1.000, 0.922, 0.804, 1.0),
    "blue": (0.000, 0.000, 1.000, 1.0),
    "blueviolet": (0.541, 0.169, 0.886, 1.0),
    "brown": (0.647, 0.165, 0.165, 1.0),
    "burlywood": (0.871, 0.722, 0.529, 1.0),
    "cadetblue": (0.373, 0.620, 0.627, 1.0),
    "chartreuse": (0.498, 1.000, 0.000, 1.0),
    "chocolate": (0.824, 0.412, 0.118, 1.0),
    "coral": (1.000, 0.498, 0.314, 1.0),
    "cornflowerblue": (0.392, 0.584, 0.929, 1.0),
    "cornsilk": (1.000, 0.973, 0.863, 1.0),
    "crimson": (0.863, 0.078, 0.235, 1.0),
    "cyan": (0.000, 1.000, 1.000, 1.0),
    "darkblue": (0.000, 0.000, 0.545, 1.0),
    "darkcyan": (0.000, 0.545, 0.545, 1.0),
    "darkgoldenrod": (0.722, 0.525, 0.043, 1.0),
    "darkgray": (0.663, 0.663, 0.663, 1.0),
    "darkgreen": (0.000, 0.392, 0.000, 1.0),
    "darkgrey": (0.663, 0.663, 0.663, 1.0),
    "darkkhaki": (0.741, 0.718, 0.420, 1.0),
    "darkmagenta": (0.545, 0.000, 0.545, 1.0),
    "darkolivegreen": (0.333, 0.420, 0.184, 1.0),
    "darkorange": (1.000, 0.549, 0.000, 1.0),
    "darkorchid": (0.600, 0.196, 0.800, 1.0),
    "darkred": (0.545, 0.000, 0.000, 1.0),
    "darksalmon": (0.914, 0.588, 0.478, 1.0),
    "darkseagreen": (0.561, 0.737, 0.561, 1.0),
    "darkslateblue": (0.282, 0.239, 0.545, 1.0),
    "darkslategray": (0.184, 0.310, 0.310, 1.0),
    "darkslategrey": (0.184, 0.310, 0.310, 1.0),
    "darkturquoise": (0.000, 0.808, 0.820, 1.0),
    "darkviolet": (0.580, 0.000, 0.827, 1.0),
    "deeppink": (1.000, 0.078, 0.576, 1.0),
    "deepskyblue": (0.000, 0.749, 1.000, 1.0),
    "dimgray": (0.412, 0.412, 0.412, 1.0),
    "dimgrey": (0.412, 0.412, 0.412, 1.0),
    "dodgerblue": (0.118, 0.565, 1.000, 1.0),
    "firebrick": (0.698, 0.133, 0.133, 1.0),
    "floralwhite": (1.000, 0.980, 0.941, 1.0),
    "forestgreen": (0.133, 0.545, 0.133, 1.0),
    "fuchsia": (1.000, 0.000, 1.000, 1.0),
    "gainsboro": (0.863, 0.863, 0.863, 1.0),
    "ghostwhite": (0.973, 0.973, 1.000, 1.0),
    "gold": (1.000, 0.843, 0.000, 1.0),
    "goldenrod": (0.855, 0.647, 0.125, 1.0),
    "gray": (0.502, 0.502, 0.502, 1.0),
    "green": (0.000, 0.502, 0.000, 1.0),
    "greenyellow": (0.678, 1.000, 0.184, 1.0),
    "grey": (0.502, 0.502, 0.502, 1.0),
    "honeydew": (0.941, 1.000, 0.941, 1.0),
    "hotpink": (1.000, 0.412, 0.706, 1.0),
    "indianred": (0.804, 0.361, 0.361, 1.0),
    "indigo": (0.294, 0.000, 0.510, 1.0),
    "ivory": (1.000, 1.000, 0.941, 1.0),
    "khaki": (0.941, 0.902, 0.549, 1.0),
    "lavender": (0.902, 0.902, 0.980, 1.0),
    "lavenderblush": (1.000, 0.941, 0.961, 1.0),
    "lawngreen": (0.486, 0.988, 0.000, 1.0),
    "lemonchiffon": (1.000, 0.980, 0.804, 1.0),
    "lightblue": (0.678, 0.847, 0.902, 1.0),
    "lightcoral": (0.941, 0.502, 0.502, 1.0),
    "lightcyan": (0.878, 1.000, 1.000, 1.0),
    "lightgoldenrodyellow": (0.980, 0.980, 0.824, 1.0),
    "lightgray": (0.827, 0.827, 0.827, 1.0),
    "lightgreen": (0.565, 0.933, 0.565, 1.0),
    "lightgrey": (0.827, 0.827, 0.827, 1.0),
    "lightpink": (1.000, 0.714, 0.757, 1.0),
    "lightsalmon": (1.000, 0.627, 0.478, 1.0),
    "lightseagreen": (0.125, 0.698, 0.667, 1.0),
    "lightskyblue": (0.529, 0.808, 0.980, 1.0),
    "lightslategray": (0.467, 0.533, 0.600, 1.0),
    "lightslategrey": (0.467, 0.533, 0.600, 1.0),
    "lightsteelblue": (0.690, 0.769, 0.871, 1.0),
    "lightyellow": (1.000, 1.000, 0.878, 1.0),
    "lime": (0.000, 1.000, 0.000, 1.0),
    "limegreen": (0.196, 0.804, 0.196, 1.0),
    "linen": (0.980, 0.941, 0.902, 1.0),
    "magenta": (1.000, 0.000, 1.000, 1.0),
    "maroon": (0.502, 0.000, 0.000, 1.0),
    "mediumaquamarine": (0.400, 0.804, 0.667, 1.0),
    "mediumblue": (0.000, 0.000, 0.804, 1.0),
    "mediumorchid": (0.729, 0.333, 0.827, 1.0),
    "mediumpurple": (0.576, 0.439, 0.859, 1.0),
    "mediumseagreen": (0.235, 0.702, 0.443, 1.0),
    "mediumslateblue": (0.482, 0.408, 0.933, 1.0),
    "mediumspringgreen": (0.000, 0.980, 0.604, 1.0),
    "mediumturquoise": (0.282, 0.820, 0.800, 1.0),
    "mediumvioletred": (0.780, 0.082, 0.522, 1.0),
    "midnightblue": (0.098, 0.098, 0.439, 1.0),
    "mintcream": (0.961, 1.000, 0.980, 1.0),
    "mistyrose": (1.000, 0.894, 0.882, 1.0),
    "moccasin": (1.000, 0.894, 0.710, 1.0),
    "navajowhite": (1.000, 0.871, 0.678, 1.0),
    "navy": (0.000, 0.000, 0.502, 1.0),
    "oldlace": (0.992, 0.961, 0.902, 1.0),
    "olive": (0.502, 0.502, 0.000, 1.0),
    "olivedrab": (0.420, 0.557, 0.137, 1.0),
    "orange": (1.000, 0.647, 0.000, 1.0),
    "orangered": (1.000, 0.271, 0.000, 1.0),
    "orchid": (0.855, 0.439, 0.839, 1.0),
    "palegoldenrod": (0.933, 0.910, 0.667, 1.0),
    "palegreen": (0.596, 0.984, 0.596, 1.0),
    "paleturquoise": (0.686, 0.933, 0.933, 1.0),
    "palevioletred": (0.859, 0.439, 0.576, 1.0),
    "papayawhip": (1.000, 0.937, 0.835, 1.0),
    "peachpuff": (1.000, 0.855, 0.725, 1.0),
    "peru": (0.804, 0.522, 0.247, 1.0),
    "pink": (1.000, 0.753, 0.796, 1.0),
    "plum": (0.867, 0.627, 0.867, 1.0),
    "powderblue": (0.690, 0.878, 0.902, 1.0),
    "purple": (0.502, 0.000, 0.502, 1.0),
    "red": (1.000, 0.000, 0.000, 1.0),
    "rosybrown": (0.737, 0.561, 0.561, 1.0),
    "royalblue": (0.255, 0.412, 0.882, 1.0),
    "saddlebrown": (0.545, 0.271, 0.075, 1.0),
    "salmon": (0.980, 0.502, 0.447, 1.0),
    "sandybrown": (0.957, 0.643, 0.376, 1.0),
    "seagreen": (0.180, 0.545, 0.341, 1.0),
    "seashell": (1.000, 0.961, 0.933, 1.0),
    "sienna": (0.627, 0.322, 0.176, 1.0),
    "silver": (0.753, 0.753, 0.753, 1.0),
    "skyblue": (0.529, 0.808, 0.922, 1.0),
    "slateblue": (0.416, 0.353, 0.804, 1.0),
    "slategray": (0.439, 0.502, 0.565, 1.0),
    "slategrey": (0.439, 0.502, 0.565, 1.0),
    "snow": (1.000, 0.980, 0.980, 1.0),
    "springgreen": (0.000, 1.000, 0.498, 1.0),
    "steelblue": (0.275, 0.510, 0.706, 1.0),
    "tan": (0.824, 0.706, 0.549, 1.0),
    "teal": (0.000, 0.502, 0.502, 1.0),
    "thistle": (0.847, 0.749, 0.847, 1.0),
    "tomato": (1.000, 0.388, 0.278, 1.0),
    "turquoise": (0.251, 0.878, 0.816, 1.0),
    "violet": (0.933, 0.510, 0.933, 1.0),
    "wheat": (0.961, 0.871, 0.702, 1.0),
    "white": (1.000, 1.000, 1.000, 1.0),
    "whitesmoke": (0.961, 0.961, 0.961, 1.0),
    "yellow": (1.000, 1.000, 0.000, 1.0),
    "yellowgreen": (0.604, 0.804, 0.196, 1.0),
    "rebeccapurple": (0.4, 0.2, 0.6, 1.0),

    # Several aliases for transparent
    "clear": (0.0, 0.0, 0.0, 0.0),
    "transparent": (0.0, 0.0, 0.0, 0.0),
    "none": (0.0, 0.0, 0.0, 0.0),
}

# Translation table for stripping extraneous characters out of names.
ignored = str.maketrans({' ': None, '-': None, '_': None})


def _parse_name(text):
    """ Parse a color name.

    Parameters
    ----------
    text : str
        A string holding a color name, including all CSS color names, plus
        any additional names found in pyface.color.color_table.  The names
        are normalized to lower case and stripped of whitespace, hyphens and
        underscores.

    Returns
    -------
    result : (space, channels), or None
        Either a tuple of the form ('rgba', channels), where channels is a
        tuple of 4 floating point values between 0.0 and 1.0, inclusive;
        or None if there is no matching color name.
    """
    text = text.lower()
    text = text.translate(ignored)
    if text in color_table:
        return 'rgba', color_table[text]
    return None


def _parse_hex(text):
    """ Parse a hex form of a color.

    Parameters
    ----------
    text : str
        A string holding a hex representation of the color in the form
        '#RGB', '#RGBA', '#RRGGBB', '#RRGGBBAA', '#RRRRGGGGBBBB', or
        '#RRRRGGGGBBBBAAAA'.

    Returns
    -------
    result : (space, channels), or None
        Either a tuple of the form (space, channels), where space is one of
        'rgb' or 'rgba' and channels is a tuple of 3 or 4 floating point
        values between 0.0 and 1.0, inclusive; or None if no hex
        representation could be matched.
    """
    text = text.strip()
    if re.match("#[0-9a-fA-F]+", text) is None:
        return None
    text = text[1:]
    if len(text) in {3, 4}:
        step = 1
    elif len(text) in {6, 8}:
        step = 2
    elif len(text) in {12, 16}:
        step = 4
    else:
        return None
    maximum = (1 << 4 * step) - 1
    channels = ints_to_channels(
        (int(text[i:i+step], 16) for i in range(0, len(text), step)),
        maximum=maximum,
    )
    space = 'rgb' if len(channels) == 3 else 'rgba'
    return space, channels


class ColorParseError(ValueError):
    """ An Exception raised when parsing fails. """
    pass


def parse_text(text):
    """ Parse a text representation of a color.

    Parameters
    ----------
    text : str
        A string holding the representation of the color.  This can be:

        - a color name, including all CSS color names, plus any additional
          names found in pyface.color.color_table.  The names are normalized
          to lower case and stripped of whitespace, hyphens and underscores.

        - a hex representation of the color in the form '#RGB', '#RGBA',
          '#RRGGBB', '#RRGGBBAA', '#RRRRGGGGBBBB', or '#RRRRGGGGBBBBAAAA'.

    Returns
    -------
    space : str
        A string describing the color space for the channels.  Will be one of
        'rgb' or 'rgba'.
    channels : tuple of floats
        The channel values as a tuple of 3 or 4 floating point values between
        0.0 and 1.0, inclusive.

    Raises
    ------
    ColorParseError
        If the string cannot be converted to a valid color.
    """
    result = None
    for parser in _parse_hex, _parse_name:
        result = parser(text)
        if result is not None:
            return result
    else:
        raise ColorParseError(
            'Unable to parse color value in string {!r}'.format(text)
        )
