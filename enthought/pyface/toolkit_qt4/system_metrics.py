#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class SystemMetrics_qt4(object):
    """ The SystemMetrics monkey patch for Qt4. """

    ###########################################################################
    # 'SystemMetrics' toolkit interface.
    ###########################################################################

    def _tk_systemmetrics_get_screen_width(self):
        """ Returns the width of the screen in pixels. """

        return QtGui.QApplication.instance().desktop().screenGeometry().width()

    def _tk_systemmetrics_get_screen_height(self):

        return QtGui.QApplication.instance().desktop().screenGeometry().height()

    def _tk_systemmetrics_get_dialog_background_color(self):
        """ Returns the background color of a standard dialog window as an RGB
        tuple.  RGB values range between 0.0-1.0 
        """

        color = QtGui.QApplication.instance().palette().color(QtGui.QPalette.Window)

        return (color.redF(), color.greenF(), color.blueF())
