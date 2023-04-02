# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Utility functions for working with wx Fonts. """


import wx


def new_font_like(font, **kw):
    """ Creates a new font, like another one, only different.  Maybe. """

    point_size = kw.get("point_size", font.GetPointSize())
    family = kw.get("family", font.GetFamily())
    style = kw.get("style", font.GetStyle())
    weight = kw.get("weight", font.GetWeight())
    underline = kw.get("underline", font.GetUnderlined())
    face_name = kw.get("face_name", font.GetFaceName())

    return wx.Font(point_size, family, style, weight, underline, face_name)
