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
and Wx Font objects, trying to keep as much similarity as possible between
them.
"""

import wx

# font weight and size features changed in wxPython 4.1/wxWidgets 3.1
wx_python_4_1 = (wx.VERSION >= (4, 1))


wx_family_to_generic_family = {
    wx.FONTFAMILY_DEFAULT: 'default',
    wx.FONTFAMILY_DECORATIVE: 'fantasy',
    wx.FONTFAMILY_ROMAN: 'serif',
    wx.FONTFAMILY_SCRIPT: 'cursive',
    wx.FONTFAMILY_SWISS: 'sans-serif',
    wx.FONTFAMILY_MODERN: 'monospace',
    wx.FONTFAMILY_TELETYPE: 'typewriter',
}
generic_family_to_wx_family = {
    'default': wx.FONTFAMILY_DEFAULT,
    'fantasy': wx.FONTFAMILY_DECORATIVE,
    'decorative': wx.FONTFAMILY_DECORATIVE,
    'serif': wx.FONTFAMILY_ROMAN,
    'roman': wx.FONTFAMILY_ROMAN,
    'cursive': wx.FONTFAMILY_SCRIPT,
    'script': wx.FONTFAMILY_SCRIPT,
    'sans-serif': wx.FONTFAMILY_SWISS,
    'swiss': wx.FONTFAMILY_SWISS,
    'monospace': wx.FONTFAMILY_MODERN,
    'modern': wx.FONTFAMILY_MODERN,
    'typewriter': wx.FONTFAMILY_TELETYPE,
    'teletype': wx.FONTFAMILY_TELETYPE,
}

if wx_python_4_1:
    weight_to_wx_weight = {
        100: wx.FONTWEIGHT_THIN,
        200: wx.FONTWEIGHT_EXTRALIGHT,
        300: wx.FONTWEIGHT_LIGHT,
        400: wx.FONTWEIGHT_NORMAL,
        500: wx.FONTWEIGHT_MEDIUM,
        600: wx.FONTWEIGHT_SEMIBOLD,
        700: wx.FONTWEIGHT_BOLD,
        800: wx.FONTWEIGHT_EXTRABOLD,
        900: wx.FONTWEIGHT_HEAVY,
        1000: wx.FONTWEIGHT_EXTRAHEAVY,
    }
    wx_weight_to_weight = {
        wx.FONTWEIGHT_THIN: 'thin',
        wx.FONTWEIGHT_EXTRALIGHT: 'extra-light',
        wx.FONTWEIGHT_LIGHT: 'light',
        wx.FONTWEIGHT_NORMAL: 'normal',
        wx.FONTWEIGHT_MEDIUM: 'medium',
        wx.FONTWEIGHT_SEMIBOLD: 'semibold',
        wx.FONTWEIGHT_BOLD: 'bold',
        wx.FONTWEIGHT_EXTRABOLD: 'extra-bold',
        wx.FONTWEIGHT_HEAVY: 'heavy',
        wx.FONTWEIGHT_EXTRAHEAVY: 'extra-heavy',
        wx.FONTWEIGHT_MAX: 'extra-heavy',
    }
else:
    weight_to_wx_weight = {
        100: wx.FONTWEIGHT_LIGHT,
        200: wx.FONTWEIGHT_LIGHT,
        300: wx.FONTWEIGHT_LIGHT,
        400: wx.FONTWEIGHT_NORMAL,
        500: wx.FONTWEIGHT_NORMAL,
        600: wx.FONTWEIGHT_BOLD,
        700: wx.FONTWEIGHT_BOLD,
        800: wx.FONTWEIGHT_BOLD,
        900: wx.FONTWEIGHT_MAX,
        1000: wx.FONTWEIGHT_MAX,
    }
    wx_weight_to_weight = {
        wx.FONTWEIGHT_LIGHT: 'light',
        wx.FONTWEIGHT_NORMAL: 'normal',
        wx.FONTWEIGHT_BOLD: 'bold',
        wx.FONTWEIGHT_MAX: 'extra-heavy',
    }

style_to_wx_style = {
    'normal': wx.FONTSTYLE_NORMAL,
    'oblique': wx.FONTSTYLE_SLANT,
    'italic': wx.FONTSTYLE_ITALIC,
}
wx_style_to_style = {value: key for key, value in style_to_wx_style.items()}


def font_to_toolkit_font(font):
    """ Convert a Pyface font to a wx.font Font.

    Wx fonts have no notion of stretch values or small-caps or overline
    variants, so these are ignored when converting.

    Parameters
    ----------
    font : pyface.font.Font
        The Pyface font to convert.

    Returns
    -------
    wx_font : wx.font.Font
        The best matching wx font.
    """
    size = int(font.size)
    for family in font.family:
        if family in generic_family_to_wx_family:
            default_family = generic_family_to_wx_family[family]
            break
    else:
        default_family = wx.FONTFAMILY_DEFAULT
    weight = weight_to_wx_weight[font.weight_]
    style = style_to_wx_style[font.style]
    underline = ('underline' in font.decorations)

    # get a default font candidate
    wx_font = wx.Font(size, default_family, style, weight, underline)
    for face in font.family:
        # don't try to match generic family
        if face in generic_family_to_wx_family:
            break
        wx_font = wx.Font(
            size, default_family, style, weight, underline, face)
        # we have a match, so stop
        if wx_font.GetFaceName().lower() == face.lower():
            break

    wx_font.SetStrikethrough('strikethrough' in font.decorations)
    return wx_font


def toolkit_font_to_properties(toolkit_font):
    """ Convert a Wx Font to a dictionary of font properties.

    Parameters
    ----------
    toolkit_font : wx.font.Font
        The Wx font to convert.

    Returns
    -------
    properties : dict
        Font properties suitable for use in creating a Pyface Font.
    """
    family = wx_family_to_generic_family[toolkit_font.GetFamily()]
    face = toolkit_font.GetFaceName()
    if wx_python_4_1:
        size = toolkit_font.GetFractionalPointSize()
    else:
        size = toolkit_font.GetPointSize()
    style = wx_style_to_style[toolkit_font.GetStyle()]
    weight = wx_weight_to_weight[toolkit_font.GetWeight()]
    decorations = set()
    if toolkit_font.GetUnderlined():
        decorations.add('underline')
    if toolkit_font.GetStrikethrough():
        decorations.add('strikethrough')

    return {
        'family': [face, family],
        'size': size,
        'weight': weight,
        'stretch': 'normal',
        'style': style,
        'variants': set(),
        'decorations': decorations,
    }
