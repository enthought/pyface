# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>

""" Utilities for handling alignment """

import wx


ALIGNMENT_TO_WX_ALIGNMENT = {
    'default': wx.TE_LEFT,
    'left': wx.TE_LEFT,
    'center': wx.TE_CENTRE,
    'right': wx.TE_RIGHT,
}
WX_ALIGNMENT_TO_ALIGNMENT = {
    0: 'default',
    wx.TE_LEFT: 'left',
    wx.TE_CENTRE: 'center',
    wx.TE_RIGHT: 'right',
}
ALIGNMENT_MASK = wx.TE_LEFT | wx.TE_CENTRE | wx.TE_RIGHT


def get_alignment_style(style_flags):
    alignment_flag = style_flags & ALIGNMENT_MASK
    return WX_ALIGNMENT_TO_ALIGNMENT[alignment_flag]


def set_alignment_style(alignment, style_flags):
    other_flags = style_flags & ~ALIGNMENT_MASK
    return other_flags | ALIGNMENT_TO_WX_ALIGNMENT[alignment]
