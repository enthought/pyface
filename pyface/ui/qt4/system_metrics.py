#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------


# Major package imports.
from pyface.qt import QtGui

# Enthought library imports.
from traits.api import HasTraits, Int, Property, provides, Tuple

# Local imports.
from pyface.i_system_metrics import ISystemMetrics, MSystemMetrics


@provides(ISystemMetrics)
class SystemMetrics(MSystemMetrics, HasTraits):
    """ The toolkit specific implementation of a SystemMetrics.  See the
    ISystemMetrics interface for the API documentation.
    """


    #### 'ISystemMetrics' interface ###########################################

    screen_width = Property(Int)

    screen_height = Property(Int)

    dialog_background_color = Property(Tuple)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_screen_width(self):
        return QtGui.QApplication.instance().desktop().screenGeometry().width()

    def _get_screen_height(self):
        return QtGui.QApplication.instance().desktop().screenGeometry().height()

    def _get_dialog_background_color(self):
        color = QtGui.QApplication.instance().palette().color(QtGui.QPalette.Window)

        return (color.redF(), color.greenF(), color.blueF())


#### EOF ######################################################################
