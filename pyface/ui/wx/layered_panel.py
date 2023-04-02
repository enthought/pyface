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


import wx
from wx.lib.scrolledpanel import ScrolledPanel

from traits.api import Int, provides

from pyface.i_layered_panel import ILayeredPanel, MLayeredPanel
from .layout_widget import LayoutWidget


@provides(ILayeredPanel)
class LayeredPanel(MLayeredPanel, LayoutWidget):
    """ A Layered panel.

    A layered panel contains one or more named layers, with only one layer
    visible at any one time (think of a 'tab' control minus the tabs!).  Each
    layer is a toolkit-specific control.

    """

    # The default style.
    STYLE = wx.CLIP_CHILDREN

    # The minimum for the panel, which is the maximum of the minimum
    # sizes of the layers
    min_width = Int(0)
    min_height = Int(0)

    # ------------------------------------------------------------------------
    # 'LayeredPanel' interface.
    # ------------------------------------------------------------------------

    def add_layer(self, name, layer):
        """ Adds a layer with the specified name.

        All layers are hidden when they are added.  Use 'show_layer' to make a
        layer visible.

        """

        # Add the layer to our sizer.
        sizer = self.control.GetSizer()
        sizer.Add(layer, 1, wx.EXPAND)

        # All layers are hidden when they are added.  Use 'show_layer' to make
        # a layer visible.
        sizer.Show(layer, False)

        # fixme: Should we warn if a layer is being overridden?
        self._layers[name] = layer

        # fixme: The minimum size stuff that was added for linux broke the
        # sizing on Windows (at least for the preference dialog).  The
        # preference dialog now sets the minimum width and height to -1 so
        # that this layout code doesn't get executed.
        if self.min_width != -1 or self.min_height != -1:
            if layer.GetSizer() is None:
                return layer

            min_size = layer.GetSizer().CalcMin()
            needs_layout = False
            if min_size.GetWidth() > self.min_width:
                self.min_width = min_size.GetWidth()
                needs_layout = True
            if min_size.GetHeight() > self.min_height:
                self.min_height = min_size.GetHeight()
                needs_layout = True

            if needs_layout:
                # Reset our size hints and relayout
                self.control.SetSizeHints(self.min_width, self.min_height)
                self.control.GetSizer().Layout()

                # fixme: Force our parent to reset it's size hints to its
                # minimum
                parent = self.control.GetParent()
                parent.GetSizer().SetSizeHints(parent)
                parent.GetSizer().Layout()

        return layer

    def show_layer(self, name):
        """ Shows the layer with the specified name. """

        # Hide the current layer (if one is displayed).
        if self.current_layer is not None:
            self._hide_layer(self.current_layer)

        # Show the specified layer.
        layer = self._show_layer(name, self._layers[name])

        return layer

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        panel = ScrolledPanel(parent, -1, style=self.STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)
        panel.SetAutoLayout(True)
        panel.SetupScrolling()

        return panel

    def _hide_layer(self, layer):
        """ Hides the specified layer. """

        sizer = self.control.GetSizer()
        sizer.Show(layer, False)
        sizer.Layout()

    def _show_layer(self, name, layer):
        """ Shows the specified layer. """

        sizer = self.control.GetSizer()
        sizer.Show(layer, True)
        sizer.Layout()

        self.current_layer = layer
        self.current_layer_name = name

        return layer
