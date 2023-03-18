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

from traits.api import Int, provides

from pyface.qt.QtGui import QStackedWidget
from pyface.i_layered_panel import ILayeredPanel, MLayeredPanel
from .layout_widget import LayoutWidget


@provides(ILayeredPanel)
class LayeredPanel(MLayeredPanel, LayoutWidget):
    """ A Layered panel.

    A layered panel contains one or more named layers, with only one layer
    visible at any one time (think of a 'tab' control minus the tabs!).  Each
    layer is a toolkit-specific control.

    """

    # The minimum sizes of the panel.  Ignored in Qt.
    min_width = Int(0)
    min_height = Int(0)

    # ------------------------------------------------------------------------
    # 'ILayeredPanel' interface.
    # ------------------------------------------------------------------------

    def add_layer(self, name, layer):
        """ Adds a layer with the specified name.

        All layers are hidden when they are added.  Use 'show_layer' to make a
        layer visible.
        """
        self.control.addWidget(layer)
        self._layers[name] = layer
        return layer

    def show_layer(self, name):
        """ Shows the layer with the specified name. """
        layer = self._layers[name]
        layer_index = self.control.indexOf(layer)
        self.control.setCurrentIndex(layer_index)
        self.current_layer = layer
        self.current_layer_name = name
        return layer

    # ------------------------------------------------------------------------
    # "IWidget" interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = QStackedWidget(parent)
        return control
