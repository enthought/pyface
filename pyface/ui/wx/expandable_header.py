# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A header for an entry in a collection of expandables.

The header provides a visual indicator of the current state, a text label,
and a 'remove' button.
"""

import warnings

import wx

from traits.api import Event, Str, Bool

from pyface.wx.util.font_helper import new_font_like
from pyface.ui_traits import Image
from .image_resource import ImageResource
from .widget import Widget


class ExpandableHeader(Widget):
    """ A header for an entry in a collection of expandables.

    The header provides a visual indicator of the current state, a text label,
    and a 'remove' button.
    """

    #: The title of the panel.
    title = Str("Panel")

    #: The carat image to show when the panel is collapsed.
    collapsed_carat_image = Image(ImageResource("carat_closed"))

    #: The carat image to show when the panel is expanded.
    expanded_carat_image = Image(ImageResource("carat_open"))

    #: Represents the current state of the panel. True means expanded.
    state = Bool(False)

    # Events ----

    #: The panel has been expanded or collapsed
    panel_expanded = Event()

    #: The panel has been closed
    panel_closed = Event()

    _CARAT_X = 4
    _CARAT_Y = 4
    _TEXT_Y = 0
    _TEXT_X_OFFSET = 10

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent=None, container=None, **traits):
        """ Creates the panel. """

        if container is not None:
            warnings.warn(
                "the container parameter is deprecated and will be "
                "removed in a future Pyface release",
                DeprecationWarning,
                stacklevel=2,
            )
            self.observe(
                lambda event: container.remove_panel(event.new),
                "panel_closed",
            )
        create = traits.pop("create", None)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        # Create the toolkit-specific control that represents the widget.
        if create:
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, code should not pass the create "
                "parameter and should instead call create() explicitly",
                DeprecationWarning,
                stacklevel=2,
            )
        elif create is not None:
            warnings.warn(
                "setting create=False is no longer required",
                DeprecationWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        collapsed_carat = self.collapsed_carat_image.create_image()
        self._collapsed_bmp = collapsed_carat.ConvertToBitmap()
        self._carat_w = self._collapsed_bmp.GetWidth()

        expanded_carat = self.expanded_carat_image.create_image()
        self._expanded_bmp = expanded_carat.ConvertToBitmap()

        # create our panel and initialize it appropriately
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN | wx.BORDER_SIMPLE)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # create the remove button
        remove = wx.BitmapButton.NewCloseButton(panel, -1)
        sizer.Add(remove, 0, wx.ALIGN_RIGHT, 5)

        # Create a suitable font.
        self._font = new_font_like(
            wx.NORMAL_FONT, point_size=wx.NORMAL_FONT.GetPointSize() - 1
        )

        height = self._get_preferred_height(parent, self.title, self._font)
        panel.SetMinSize((-1, height+2))

        panel.Bind(wx.EVT_PAINT, self._on_paint)
        panel.Bind(wx.EVT_LEFT_DOWN, self._on_down)
        panel.Bind(wx.EVT_BUTTON, self._on_remove)

        return panel

    def _get_preferred_height(self, parent, text, font):
        """ Calculates the preferred height of the widget. """

        dc = wx.MemoryDC()

        dc.SetFont(font)
        metrics = dc.GetFontMetrics()
        text_h = metrics.height + 2 * self._TEXT_Y

        # add in height of buttons
        carat_h = self._collapsed_bmp.GetHeight() + 2 * self._CARAT_Y

        return max(text_h, carat_h)

    def _draw_carat_button(self, dc):
        """ Draws the button at the correct coordinates. """

        if self.state:
            bmp = self._expanded_bmp
        else:
            bmp = self._collapsed_bmp

        dc.DrawBitmap(bmp, self._CARAT_X, self._CARAT_Y, True)

    def _draw_title(self, dc):
        """ Draws the text label for the header. """
        dc.SetFont(self._font)

        # Render the text.
        dc.DrawText(
            self.title, self._carat_w + self._TEXT_X_OFFSET, self._TEXT_Y
        )

    def _draw(self, dc):
        """ Draws the control. """

        # Draw the title text
        self._draw_title(dc)

        # Draw the carat button
        self._draw_carat_button(dc)

    # ------------------------------------------------------------------------
    # wx event handlers.
    # ------------------------------------------------------------------------

    def _on_paint(self, event):
        """ Called when the background of the panel is erased. """

        # print('ImageButton._on_erase_background')
        dc = wx.PaintDC(self.control)
        self._draw(dc)

    def _on_down(self, event):
        """ Called when button is pressed. """

        self.state = not self.state
        self.control.Refresh()

        # fire an event so any listeners can pick up the change
        self.panel_expanded = self
        event.Skip()

    def _on_remove(self, event):
        """ Called when remove button is pressed. """
        self.panel_closed = self
