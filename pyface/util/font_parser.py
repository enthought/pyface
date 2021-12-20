# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


GENERIC_FAMILIES = {
    'default', 'fantasy', 'decorative', 'serif', 'roman', 'cursive', 'script',
    'sans-serif', 'swiss', 'monospace', 'modern', 'typewriter', 'teletype'
}
WEIGHTS = {'thin', 'extra-light', 'light', 'regular', 'medium', 'demi-bold',
    'bold', 'extra-bold', 'heavy', 'extra-heavy'}
STRETCHES = {'ultra-condensed', 'extra-condensed', 'condensed',
    'semi-condensed', 'semi-expanded', 'expanded', 'extra-expanded',
    'ultra-expanded'}
STYLES = {'italic', 'oblique'}
VARIANTS = {'small-caps'}
DECORATIONS = {'underline', 'strikethrough', 'overline'}
NOISE = {'pt', 'point', 'px', 'family'}


class FontParseError(ValueError):
    """An exception raised when font parsing fails."""
    pass


def simple_parser(description):
    """An extremely simple font description parser.

    This is roughly compatible with the various ad-hoc parsers in TraitsUI
    and Kiva, allowing for the slight differences between them and adding
    support for additional options supported by Pyface fonts, such as stretch
    and variants.

    Parameters
    ----------
    description : str
        The font description to be parsed.

    Returns
    -------
    properties : dict
        Font properties suitable for use in creating a Pyface Font.

    Notes
    -----
    This is not a particularly good parser, as it will fail to properly
    parse something like "10 pt times new roman" or "14 pt computer modern"
    since they have generic font names as part of the font face name.
    """
    face = []
    generic_family = ""
    size = None
    weight = "normal"
    stretch = "normal"
    style = "normal"
    variants = set()
    decorations = set()
    for word in description.lower().split():
        if word in NOISE:
            continue
        elif word in GENERIC_FAMILIES:
            generic_family = word
        elif word in WEIGHTS:
            weight = word
        elif word in STRETCHES:
            stretch = word
        elif word in STYLES:
            style = word
        elif word in VARIANTS:
            variants.add(word)
        elif word in DECORATIONS:
            decorations.add(word)
        else:
            if size is None:
                try:
                    size = int(word)
                    continue
                except ValueError:
                    pass
            face.append(word)

    family = []
    if face:
        family.append(" ".join(face))
    if generic_family:
        family.append(generic_family)
    if not family:
        family = ["default"]

    return {
        'family': family,
        'size': size,
        'weight': weight,
        'stretch': stretch,
        'style': style,
        'variants': variants,
        'decorations': decorations,
    }
