# (C) Copyright 2004-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines a wxPython ImageControl widget that is used by various Widgets.
"""


import wx


class ImageControl(wx.Window):
    """A wxPython control that displays an image.
    """

    def __init__(self, parent, bitmap=None, padding=10):
        """Initializes the object."""
        if bitmap is not None:
            size = wx.Size(
                bitmap.GetWidth() + padding, bitmap.GetHeight() + padding
            )
        else:
            size = wx.Size(32 + padding, 32 + padding)

        wx.Window.__init__(self, parent, -1, size=size,)
        self._bitmap = bitmap

        # Set up the 'paint' event handler:
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def SetBitmap(self, bitmap=None):
        """Sets the bitmap image."""
        if bitmap is not None:
            if bitmap != self._bitmap:
                self._bitmap = bitmap
                self.Refresh()
        else:
            self._bitmap = None

    def GetBitmap(self):
        """Gets the bitmap image."""
        return self._bitmap

    def _on_paint(self, event=None):
        """Handles the control being re-painted."""
        wdc = wx.PaintDC(self)
        wdx, wdy = self.GetClientSize()
        bitmap = self._bitmap
        if bitmap is None:
            return
        bdx = bitmap.GetWidth()
        bdy = bitmap.GetHeight()
        wdc.DrawBitmap(bitmap, (wdx - bdx) // 2, (wdy - bdy) // 2, True)
