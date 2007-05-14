#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  Author: Scott Swarts <swarts@enthought.com>
#
#-----------------------------------------------------------------------------

"""A widget containing a chaco plottable.
"""

# Standard library imports.

# Major packages.

# Enthought library imports
from enthought.chaco.plottable import Plottable
from enthought.chaco.plot_component import PlotComponent
from enthought.enable.wx import Window

from enthought.traits.api import Instance, Tuple

# Application specific imports.

# Local imports.

from widget import Widget

##############################################################################
# class 'PlotWidget'
##############################################################################

class PlotWidget(Widget):
    """A widget containing a chaco plottable.
    """

    ##########################################################################
    # Traits
    ##########################################################################

    ### 'PlotWidget' interface ###############################################

    # The plottable to show
    plottable = Instance(Plottable)

    # The size
    size = Tuple(400,400)

    # The underlying enable window
    enable_window = Instance(Window)

    ##########################################################################
    # 'object' interface
    ##########################################################################

    def __init__(self, parent, plottable, **traits):
        super(PlotWidget, self).__init__(plottable=plottable,
                                         **traits)

        self.control = self._create_control(parent)

    ##########################################################################
    # 'PlotWidget' interface
    ##########################################################################

    def _create_control(self, parent):
        """
        Creates the enable widow and sets the control.
        """
        component = PlotComponent(self.plottable)
        self.enable_window = Window(parent, component=component)
        self.enable_window.control.SetSize(self.size)
        return self.enable_window.control

    ##########################################################################
    # Trait handlers
    ##########################################################################

    def _plottable_changed(self, new_plottable):
        """
        If we already have created the window, set the plottable.
        """
        if self.enable_window is not None:
            self.enable_window.component.component = new_plottable
            new_plottable.update()

    def _size_changed(self, new_size):
        """
        If we alread have created the window, change the size.
        """
        if self.enable_window is not None:
            self.enable_window.control.SetSize(new_size)


#### EOF ######################################################################
