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
""" A header for an entry in a collection of expandables. The header
provides a visual indicator of the current state, a text label, and a
'remove' button. """
from __future__ import absolute_import

# Major package imports.
import wx

# Enthought library imports.
from traits.api import Instance, Event, Str, Bool

# local imports
from pyface.wx.util.font_helper import new_font_like
from .image_resource import ImageResource
from .widget import Widget


class ExpandableHeader(Widget):
    """ A header for an entry in a collection of expandables. The header
    provides a visual indicator of the current state, a text label, and a
    'remove' button. """

    # The title of the panel.
    title = Str('Panel')

    # The carat image to show when the panel is collapsed.
    collapsed_carat_image = Instance(ImageResource, ImageResource('carat_closed'))
    # The carat image to show when the panel is expanded.
    expanded_carat_image = Instance(ImageResource, ImageResource('carat_open'))
    # The backing header image when the mouse is elsewhere
    header_bar_image = Instance(ImageResource,
                                ImageResource('panel_gradient'))
    # The backing header image when the mouse is over
    header_mouseover_image = Instance(ImageResource,
                                      ImageResource('panel_gradient_over'))

    # The carat image to show when the panel is expanded.
    remove_image = Instance(ImageResource, ImageResource('close'))

    # Represents the current state of the button. True means pressed.
    state = Bool(False)

    #### Events ####

    # The panel has been expanded or collapsed
    panel_expanded = Event


    _CARAT_X = 4
    _CARAT_Y = 2
    _TEXT_Y = 0
    _TEXT_X_OFFSET = 10

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, parent, container, **traits):
        """ Creates the panel. """

        # Base class constructor.
        super(ExpandableHeader, self).__init__(**traits)

        # Create the toolkit-specific control that represents the widget.
        self.control = self._create_control(parent)

        self._container = container
        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        collapsed_carat = self.collapsed_carat_image.create_image()
        self._collapsed_bmp = collapsed_carat.ConvertToBitmap()
        self._carat_w = self._collapsed_bmp.GetWidth()

        expanded_carat = self.expanded_carat_image.create_image()
        self._expanded_bmp = expanded_carat.ConvertToBitmap()

        header_bar = self.header_bar_image.create_image()
        self._header_bmp = header_bar.ConvertToBitmap()

        header_bar_over = self.header_mouseover_image.create_image()
        self._header_mouseover_bmp = header_bar_over.ConvertToBitmap()

        self._background_bmp = self._header_bmp

        close_image = self.remove_image.create_image()
        self._remove_bmp = close_image.ConvertToBitmap()

        # create our panel and initialize it appropriately
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # needed on GTK systems for EVT_ERASE_BACKGROUND to work
        panel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        # create the remove button
        remove = wx.BitmapButton(panel, -1, self._remove_bmp, style=0,
                                 pos=(-1, 3))
        sizer.Add(remove, 0, wx.ALIGN_RIGHT, 5)

        # Create a suitable font.
        self._font = new_font_like(wx.NORMAL_FONT,
                                   point_size=wx.NORMAL_FONT.GetPointSize()- 1)

        height = self._get_preferred_height(parent, self.title, self._font)
        panel.SetSize((-1, height))

        wx.EVT_ERASE_BACKGROUND(panel, self._on_erase_background)
        wx.EVT_ENTER_WINDOW(panel, self._on_enter_leave)
        wx.EVT_LEAVE_WINDOW(panel, self._on_enter_leave)
        wx.EVT_LEFT_DOWN(panel, self._on_down)
        wx.EVT_RIGHT_DOWN(panel, self._on_down)

        wx.EVT_BUTTON(panel, remove.GetId(), self._on_remove)

        return panel

    def _get_preferred_height(self, parent, text, font):
        """ Calculates the preferred height of the widget. """

        dc = wx.MemoryDC()

        dc.SetFont(font)
        text_w, text_h = dc.GetTextExtent(text)
        text_h = text_h + self._TEXT_Y

        # add in width of buttons
        carat_h = self._collapsed_bmp.GetHeight() + self._CARAT_Y

        return max(text_h, carat_h)

    def _draw_carat_button(self, dc):
        """ Draws the button at the correct coordinates. """

        if self.state:
            bmp = self._expanded_bmp
        else:
            bmp = self._collapsed_bmp

        dc.DrawBitmap(bmp, self._CARAT_X, self._CARAT_Y, True)

        return

    def _tile_background_image(self, dc, width, height):
        """ Tiles the background image. """

        w = self._background_bmp.GetWidth()
        h = self._background_bmp.GetHeight()

        x = 0
        while x < width:
            y = 0
            while y < height:
                dc.DrawBitmap(self._background_bmp, x, y)

                y = y + h

            x = x + w

        return

    def _draw_title(self, dc):
        """ Draws the text label for the header. """
        dc.SetFont(self._font)

        # Render the text.
        dc.DrawText(self.title, self._carat_w + self._TEXT_X_OFFSET,
                    self._TEXT_Y)

    def _draw(self, dc):
        """ Draws the control. """

        size = self.control.GetClientSize()

        # Tile the background image.
        self._tile_background_image(dc, size.width, size.height)

        self._draw_title(dc)

        # Draw the carat button
        self._draw_carat_button(dc)

        return

    ###########################################################################
    # wx event handlers.
    ###########################################################################

    def _on_erase_background(self, event):
        """ Called when the background of the panel is erased. """

        #print 'ImageButton._on_erase_background'
        dc = event.GetDC()
        self._draw(dc)
        return

    def _on_enter_leave(self, event):
        """ Called when button is pressed. """

        #print 'ExpandableHeader._on_enter_leave'
        if event.Entering():
            self._background_bmp = self._header_mouseover_bmp
        else:
            self._background_bmp = self._header_bmp

        self.control.Refresh()
        event.Skip()

    def _on_down(self, event):
        """ Called when button is pressed. """

        #print 'ImageButton._on_down'
        self.state = not self.state
        self.control.Refresh()

        # fire an event so any listeners can pick up the change
        self.panel_expanded = self
        event.Skip()

    def _on_remove(self, event):
        """ Called when remove button is pressed. """

        self._container.remove_panel(self.title)
