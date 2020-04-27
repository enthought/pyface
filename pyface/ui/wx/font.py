

import wx

from pyface.font import Font


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
}

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
}

style_to_wx_style = {
    'normal': wx.FONTSTYLE_NORMAL,
    'oblique': wx.FONTSTYLE_SLANT,
    'italic': wx.FONTSTYLE_ITALIC,
}
wx_style_to_style = {value: key for key, value in style_to_wx_style.items()}


def font_to_toolkit_font(font):
    """ Convert a Pyface font to a wx.font Font.

    Wx fonts have no notion of stretch values or small-caps or overline variants,
    so these are ignored when converting.

    Parameters
    ----------
    font : pyface.font.Font
        The Pyface font to convert.

    Returns
    -------
    wx_font : wx.font.Font
        The best matching wx font.
    """
    size = font.size
    for family in font.family:
        if family in generic_family_to_wx_family:
            family = generic_family_to_wx_family[family]
            break
    else:
        family = wx.FONTFAMILY_DEFAULT
    weight = weight_to_wx_weight[font.weight_]
    style = style_to_wx_style[font.style]
    underline = ('underline' in font.variants)

    # get a default font candidate
    wx_font = wx.Font(size, family, style, weight, underline)
    for face in font.family:
        # don't try to match generic family
        if face in generic_family_to_wx_family:
            break
        wx_font = wx.Font(size, family, style, weight, underline, face)
        # we have a match, so stop
        if wx_font.GetFaceName().lower() == face.lower():
            break

    wx_font.SetStrikethrough('strikethrough' in font.variants)
    return wx_font


def toolkit_font_to_traits(toolkit_font):
    family = wx_family_to_generic_family[toolkit_font.GetFamily()]
    face = toolkit_font.GetFaceName()
    size = toolkit_font.GetFractionalPointSize()
    style = wx_style_to_style[toolkit_font.GetStyle()]
    weight = wx_weight_to_weight[toolkit_font.GetWeight()]
    variants = set()
    if toolkit_font.GetUnderline():
        variants.add('underline')
    if toolkit_font.GetStrikethrough():
        variants.add('strikethrough')

    return {
        'family': [face, family],
        'size': size,
        'weight': weight,
        'stretch': 'normal',
        'style': style,
        'variants': variants,
    }
