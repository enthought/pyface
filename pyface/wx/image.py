# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import os

import wx

from traits.util.resource import get_path


def get_bitmap(root, name):
    """
    Convenience function that returns a bitmap
    root - either an instance of a class or a path
    name - name of png file to load
    """
    path = os.path.join(get_path(root), name)
    bmp = wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
    return bmp
