# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Interace and mixins for layered panels.

A layered panel contains one or more named layers, with only one layer
visible at any one time (think of a 'tab' control minus the tabs!).
"""

import warnings

from traits.api import Any, Dict, HasTraits, Interface, Str


class ILayeredPanel(Interface):
    """ A Layered panel.

    A layered panel contains one or more named layers, with only one layer
    visible at any one time (think of a 'tab' control minus the tabs!).  Each
    layer is a toolkit-specific control.

    """

    # "ILayeredPanel' interface --------------------------------------------

    # The toolkit-specific control of the currently displayed layer.
    current_layer = Any()

    # The name of the currently displayed layer.
    current_layer_name = Str()

    # ------------------------------------------------------------------------
    # 'ILayeredPanel' interface.
    # ------------------------------------------------------------------------

    def add_layer(self, name, layer):
        """ Adds a layer with the specified name.

        All layers are hidden when they are added.  Use 'show_layer' to make a
        layer visible.

        """

    def show_layer(self, name):
        """ Shows the layer with the specified name. """

    def has_layer(self, name):
        """ Does the panel contain a layer with the specified name? """


class MLayeredPanel(HasTraits):
    """ A Layered panel mixin.

    A layered panel contains one or more named layers, with only one layer
    visible at any one time (think of a 'tab' control minus the tabs!).  Each
    layer is a toolkit-specific control.
    """

    # "ILayeredPanel' interface --------------------------------------------

    # The toolkit-specific control of the currently displayed layer.
    current_layer = Any()

    # The name of the currently displayed layer.
    current_layer_name = Str()

    # Private traits -------------------------------------------------------

    # The a map of layer names to toolkit controls in the panel.
    _layers = Dict(Str)

    # ------------------------------------------------------------------------
    # 'ILayeredPanel' interface.
    # ------------------------------------------------------------------------

    def has_layer(self, name):
        """ Does the panel contain a layer with the specified name? """
        return name in self._layers

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent=None, **traits):
        """ Creates a new LayeredPanel. """

        create = traits.pop("create", None)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        if create:
            # Create the toolkit-specific control that represents the widget.
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
