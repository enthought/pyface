# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A Layered panel. """

import warnings

import wx

from traits.api import Dict, Str

from pyface.ui_traits import Image
from .expandable_header import ExpandableHeader
from .image_resource import ImageResource
from .layout_widget import LayoutWidget


class ExpandablePanel(LayoutWidget):
    """ An expandable panel. """

    # The default style.
    STYLE = wx.CLIP_CHILDREN

    collapsed_image = Image(ImageResource("mycarat1"))
    expanded_image = Image(ImageResource("mycarat2"))

    _layers = Dict(Str)

    _headers = Dict(Str)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent=None, **traits):
        """ Creates a new LayeredPanel. """

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
    # 'Expandale' interface.
    # ------------------------------------------------------------------------

    def add_panel(self, name, layer):
        """ Adds a layer with the specified name.

        All layers are hidden when they are added.  Use 'show_layer' to make a
        layer visible.

        """

        parent = self.control
        sizer = self.control.GetSizer()

        # Add the heading text.
        header = self._create_header(parent, text=name)
        sizer.Add(header, 0, wx.EXPAND)

        # Add the layer to our sizer.
        sizer.Add(layer, 1, wx.EXPAND)

        # All layers are hidden when they are added.  Use 'show_layer' to make
        # a layer visible.
        sizer.Show(layer, False)

        # fixme: Should we warn if a layer is being overridden?
        self._layers[name] = layer

        return layer

    def remove_panel(self, name):
        """ Removes a layer and its header from the container."""

        if name not in self._layers:
            return

        sizer = self.control.GetSizer()
        panel = self._layers[name]
        header = self._headers[name]
        # sizer.Remove(panel)
        panel.Destroy()
        # sizer.Remove(header)
        header.Destroy()

        sizer.Layout()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        panel = wx.Panel(parent, -1, style=self.STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        return panel

    def _create_header(self, parent, text):
        """ Creates a panel header. """

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)

        # Add the panel header.
        heading = ExpandableHeader(panel, title=text)
        heading.create()
        sizer.Add(heading.control, 1, wx.EXPAND)

        # connect observers
        heading.observe(self._on_button, "panel_expanded")
        heading.observe(self._on_panel_closed, "panel_closed")

        # Resize the panel to match the sizer's minimum size.
        sizer.Fit(panel)

        # hang onto it for when we destroy
        self._headers[text] = panel

        return panel

    # event handlers ----------------------------------------------------

    def _on_button(self, event):
        """ called when one of the expand/contract buttons is pressed. """

        header = event.new
        name = header.title
        visible = header.state

        sizer = self.control.GetSizer()
        sizer.Show(self._layers[name], visible)
        sizer.Layout()

        # fixme: Errrr, maybe we can NOT do this!
        w, h = self.control.GetSize().Get()
        self.control.SetSize((w + 1, h + 1))
        self.control.SetSize((w, h))

    def _on_panel_closed(self, event):
        """ Called when the close button is clicked in a header. """

        header = event.new
        name = header.title
        self.remove_panel(name)
