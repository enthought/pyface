#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


SEVERITY_TO_ICON_MAP = {
    'information':  QtGui.QMessageBox.Information,
    'warning':      QtGui.QMessageBox.Warning,
    'error':        QtGui.QMessageBox.Critical
}


class MessageDialog_qt4(object):
    """ The MessageDialog monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """Create the toolkit-specific control that represents the window. """

        return QtGui.QMessageBox(SEVERITY_TO_ICON_MAP[self.severity],
                self.title, self.message, QtGui.QMessageBox.Ok, parent)
