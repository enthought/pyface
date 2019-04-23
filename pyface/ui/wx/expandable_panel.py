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
""" A Layered panel. """
from __future__ import absolute_import

# Major package imports.
import wx

from traits.api import Instance

# Local imports.
from .expandable_header import ExpandableHeader
from .image_resource import ImageResource
from .widget import Widget


class ExpandablePanel(Widget):
    """ An expandable panel. """

    # The default style.
    STYLE = wx.CLIP_CHILDREN

    collapsed_image = Instance(ImageResource, ImageResource('mycarat1'))
    expanded_image = Instance(ImageResource, ImageResource('mycarat2'))

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, parent, **traits):
        """ Creates a new LayeredPanel. """

        # Base class constructor.
        super(ExpandablePanel, self).__init__(**traits)

        # Create the toolkit-specific control that represents the widget.
        self.control = self._create_control(parent)

        # The layers in the panel.
        #
        # { str name : wx.Window layer }
        self._layers = {}
        self._headers = {}

        return

    ###########################################################################
    # 'Expandale' interface.
    ###########################################################################

    def add_panel(self, name, layer):
        """ Adds a layer with the specified name.

        All layers are hidden when they are added.  Use 'show_layer' to make a
        layer visible.

        """

        parent = self.control
        sizer  = self.control.GetSizer()

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
        sizer.Remove(panel)
        panel.Destroy()
        sizer.Remove(header)
        header.Destroy()

        sizer.Layout()

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

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
        heading = ExpandableHeader(panel, self,
                                   title = text)
        sizer.Add(heading.control, 1, wx.EXPAND)

        heading.on_trait_change(self._on_button, 'panel_expanded')

        # Resize the panel to match the sizer's minimum size.
        sizer.Fit(panel)

        # hang onto it for when we destroy
        self._headers[text] = panel

        return panel

    #### wx event handlers ####################################################

    def _on_button(self, event):
        """ called when one of the expand/contract buttons is pressed. """

        header = event
        name = header.title
        visible = header.state

        sizer = self.control.GetSizer()
        sizer.Show(self._layers[name], visible)
        sizer.Layout()

        # fixme: Errrr, maybe we can NOT do this!
        w, h = self.control.GetSize()
        self.control.SetSize((w+1, h+1))
        self.control.SetSize((w, h))
