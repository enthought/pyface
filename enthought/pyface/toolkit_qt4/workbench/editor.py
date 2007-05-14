#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


class Editor_qt4(object):
    """ The Editor monkey patch for Qt4. """

    ###########################################################################
    # 'Editor' toolkit interface.
    ###########################################################################

    def _tk_editor_create(self, parent):
        """ Create a default control. """

        panel = QtGui.QWidget(parent)
        pal = panel.palette()
        pal.setColour(QtGui.QPalette.Window, QtCore.Qt.red)
        panel.setPalette(pal)
        panel.setAutoFillBackground(True)
        panel.resize(100, 200)

        return panel

    def _tk_editor_destroy(self):
        """ Destroy the control. """

        self.control.deleteLater()

    def _tk_editor_set_focus(self):
        """ Set the focus to the control. """

        self.control.setFocus()
