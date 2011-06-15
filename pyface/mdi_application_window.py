#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" An MDI top-level application window. """
from __future__ import absolute_import

# Major package imports.
import wx

# Enthought library imports.
from traits.api import Bool, Instance, Int, Tuple

# Local imports.
from .application_window import ApplicationWindow
from .image_resource import ImageResource

try:
    import wx.aui
    AUI = True
except:
    AUI = False


class MDIApplicationWindow(ApplicationWindow):
    """ An MDI top-level application window.

    The application window has support for a menu bar, tool bar and a status
    bar (all of which are optional).

    Usage: Create a sub-class of this class and override the protected
    '_create_contents' method.

    """

    #### 'MDIApplicationWindow' interface #####################################

    # The workarea background image.
    background_image = Instance(ImageResource, ImageResource('background'))

    # Should we tile the workarea  background image?  The alternative is to
    # scale it.  Be warned that scaling the image allows for 'pretty' images,
    # but is MUCH slower than tiling.
    tile_background_image = Bool(True)

    # WX HACK FIXME
    # UPDATE: wx 2.6.1 does NOT fix this issue.
    _wx_offset = Tuple(Int, Int)

    ###########################################################################
    # 'MDIApplicationWindow' interface.
    ###########################################################################

    def create_child_window(self, title=None, is_mdi=True, float=True):
        """ Create a child window. """
        if title is None:
            title = self.title

        if is_mdi:
            return wx.MDIChildFrame(self.control, -1, title)
        else:
            if float:
                style = wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT
            else:
                style = wx.DEFAULT_FRAME_STYLE
            return wx.Frame(self.control, -1, title, style=style)

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Create the contents of the MDI window. """

        # Create the 'trim' widgets (menu, tool and status bars etc).
        self._create_trim_widgets(self.control)

        # The work-area background image (it can be tiled or scaled).
        self._image = self.background_image.create_image()
        self._bmp = self._image.ConvertToBitmap()

        # Frame events.
        #
        # We respond to size events to layout windows around the MDI frame.
        wx.EVT_SIZE(self.control, self._on_size)

        # Client window events.
        client_window = self.control.GetClientWindow()
        wx.EVT_ERASE_BACKGROUND(client_window, self._on_erase_background)

        self._wx_offset = client_window.GetPositionTuple()

        if AUI:
            # Let the AUI manager look after the frame.
            self._aui_manager.SetManagedWindow(self.control)

        contents = super(MDIApplicationWindow, self)._create_contents(parent)

        return contents

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the window. """

        control = wx.MDIParentFrame(
            parent, -1, self.title, style=wx.DEFAULT_FRAME_STYLE,
            size=self.size, pos=self.position
        )

        return control

    ###########################################################################
    # Private interface.
    ###########################################################################


    def _tile_background_image(self, dc, width, height):
        """ Tiles the background image. """

        w = self._bmp.GetWidth()
        h = self._bmp.GetHeight()

        x = 0
        while x < width:
            y = 0
            while y < height:
                dc.DrawBitmap(self._bmp, x, y)
                y = y + h

            x = x + w

        return

    def _scale_background_image(self, dc, width, height):
        """ Scales the background image. """

        # Scale the image (if necessary).
        image = self._image
        if image.GetWidth() != width or image.GetHeight()!= height:
            image = self._image.Copy()
            image.Rescale(width, height)

        # Convert it to a bitmap and draw it.
        dc.DrawBitmap(image.ConvertToBitmap(), 0, 0)

        return

    ##### wx event handlers ###################################################

    def _on_size(self, event):
        """ Called when the frame is resized. """

        wx.LayoutAlgorithm().LayoutMDIFrame(self.control)

        return

    def _on_erase_background(self, event):
        """ Called when the background of the MDI client window is erased. """

        # fixme: Close order...
        if self.control is None:
            return

        frame = self.control

        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(frame.GetClientWindow())

        size = frame.GetClientSize()

        # Currently you have two choices, tile the image or scale it.  Be
        # warned that scaling is MUCH slower than tiling.
        if self.tile_background_image:
            self._tile_background_image(dc, size.width, size.height)

        else:
            self._scale_background_image(dc, size.width, size.height)
