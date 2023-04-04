# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Font conversion utilities

This module provides facilities for converting between pyface Font objects
and Qt QFont objects, trying to keep as much similarity as possible between
them.
"""

from pyface.qt.QtGui import QFont


qt_family_to_generic_family = {
    QFont.StyleHint.AnyStyle: 'default',
    QFont.StyleHint.System: 'default',
    QFont.Decorative: 'fantasy',
    QFont.Serif: 'serif',
    QFont.StyleHint.Cursive: 'cursive',
    QFont.SansSerif: 'sans-serif',
    QFont.StyleHint.Monospace: 'monospace',
    QFont.TypeWriter: 'typewriter',
}
generic_family_to_qt_family = {
    'default': QFont.StyleHint.System,
    'fantasy': QFont.Decorative,
    'decorative': QFont.Decorative,
    'serif': QFont.Serif,
    'roman': QFont.Serif,
    'cursive': QFont.StyleHint.Cursive,
    'script': QFont.StyleHint.Cursive,
    'sans-serif': QFont.SansSerif,
    'swiss': QFont.SansSerif,
    'monospace': QFont.StyleHint.Monospace,
    'modern': QFont.StyleHint.Monospace,
    'typewriter': QFont.TypeWriter,
    'teletype': QFont.TypeWriter,
}

weight_to_qt_weight = {
    100: QFont.Weight.Thin,
    200: QFont.Weight.ExtraLight,
    300: QFont.Weight.Light,
    400: QFont.Weight.Normal,
    500: QFont.Weight.Medium,
    600: QFont.Weight.DemiBold,
    700: QFont.Weight.Bold,
    800: QFont.Weight.ExtraBold,
    900: QFont.Weight.Black,
    1000: 99,
}
qt_weight_to_weight = {
    QFont.Weight.Thin: 'thin',
    QFont.Weight.ExtraLight: 'extra-light',
    QFont.Weight.Light: 'light',
    QFont.Weight.Normal: 'normal',
    QFont.Weight.Medium: 'medium',
    QFont.Weight.DemiBold: 'demi-bold',
    QFont.Weight.Bold: 'bold',
    QFont.Weight.ExtraBold: 'extra-bold',
    QFont.Weight.Black: 'black',
    99: 'extra-heavy',
}

style_to_qt_style = {
    'normal': QFont.Style.StyleNormal,
    'oblique': QFont.Style.StyleOblique,
    'italic': QFont.Style.StyleItalic,
}
qt_style_to_style = {value: key for key, value in style_to_qt_style.items()}


def font_to_toolkit_font(font):
    """ Convert a Pyface font to a Qfont.

    Parameters
    ----------
    font : pyface.font.Font
        The Pyface font to convert.

    Returns
    -------
    qt_font : QFont
        The best matching Qt font.
    """
    qt_font = QFont()
    families = []
    default_family = None

    for family in font.family:
        if family not in generic_family_to_qt_family:
            families.append(family)
        elif default_family is None:
            default_family = family

    if families and hasattr(qt_font, 'setFamilies'):
        # Qt 5.13 and later
        qt_font.setFamilies(families)
    elif families:
        qt_font.setFamily(families[0])
        # Note: possibily could use substitutions here,
        # but not sure if global (which would be bad, so we don't)

    if default_family is not None:
        qt_font.setStyleHint(generic_family_to_qt_family[default_family])

    qt_font.setPointSizeF(font.size)
    qt_font.setWeight(weight_to_qt_weight[font.weight_])
    qt_font.setStretch(int(font.stretch))
    qt_font.setStyle(style_to_qt_style[font.style])
    qt_font.setUnderline('underline' in font.decorations)
    qt_font.setStrikeOut('strikethrough' in font.decorations)
    qt_font.setOverline('overline' in font.decorations)
    if 'small-caps' in font.variants:
        qt_font.setCapitalization(QFont.Capitalization.SmallCaps)
    return qt_font


def toolkit_font_to_properties(toolkit_font):
    """ Convert a QFont to a dictionary of font properties.

    Parameters
    ----------
    toolkit_font : QFont
        The Qt QFont to convert.

    Returns
    -------
    properties : dict
        Font properties suitable for use in creating a Pyface Font.
    """
    family = []

    if toolkit_font.family():
        family.append(toolkit_font.family())
    if hasattr(toolkit_font, 'families'):
        # Qt 5.13 and later
        family.extend(toolkit_font.families())
    family.append(qt_family_to_generic_family[toolkit_font.styleHint()])

    size = toolkit_font.pointSizeF()
    style = qt_style_to_style[toolkit_font.style()]
    weight = map_to_nearest(toolkit_font.weight(), qt_weight_to_weight)
    stretch = toolkit_font.stretch()
    if stretch == 0:
        # stretch 0 means any stretch is allowed, we default to no stretch
        stretch = 100.0
    variants = set()
    if toolkit_font.capitalization() == QFont.Capitalization.SmallCaps:
        variants.add('small-caps')
    decorations = set()
    if toolkit_font.underline():
        decorations.add('underline')
    if toolkit_font.strikeOut():
        decorations.add('strikethrough')
    if toolkit_font.overline():
        decorations.add('overline')

    return {
        'family': family,
        'size': size,
        'weight': weight,
        'stretch': stretch,
        'style': style,
        'variants': variants,
        'decorations': decorations,
    }


def map_to_nearest(target, mapping):
    """ Given mapping with keys from 0 and 99, return closest value.

    Parameters
    ----------
    target : int
        The value to map.
    mapping : dict
        A dictionary with integer keys ranging from 0 to 99.

    Returns
    -------
    value : Any
        The value corresponding to the nearest key.  In the case of a tie,
        the first value is returned.
    """
    if target in mapping:
        return mapping[target]

    distance = 100
    nearest = None
    for key in mapping:
        if abs(target - key) < distance:
            distance = abs(target - key)
            nearest = key
    return mapping[nearest]
