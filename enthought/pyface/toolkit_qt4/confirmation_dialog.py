#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui

# Enthought library imports.
from enthought.pyface.api import YES, NO, CANCEL


class ConfirmationDialog_qt4(object):
    """ The ConfirmationDialog monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create the toolkit-specific control that represents the window. """

        dlg = QtGui.QMessageBox(parent)
        dlg.setWindowTitle(self.title)

        return dlg

    ###########################################################################
    # 'Dialog' toolkit interface.
    ###########################################################################

    def _tk_dialog_create_area(self, parent):
        """ Creates the main content of the dialog. """

        if self.image is None:
            parent.setIcon(QtGui.QMessageBox.Question)
        else:
            parent.setIconPixmap(self.image.create_image())

        parent.setText(self.message)

        return None

    def _tk_dialog_create_buttons(self, parent):
        """ Creates the buttons. """

        # 'Yes' button.
        if self.yes_label:
            btn = parent.addButton(self.yes_label, QtGui.QMessageBox.YesRole)
        else:
            btn = parent.addButton(QtGui.QMessageBox.Yes)

        if self.default == YES:
            parent.setDefaultButton(btn)

        # 'No' button.
        if self.no_label:
            btn = parent.addButton(self.no_label, QtGui.QMessageBox.NoRole)
        else:
            btn = parent.addButton(QtGui.QMessageBox.No)

        if self.default == NO:
            parent.setDefaultButton(btn)

        # 'Cancel' button.
        if self.cancel:
            if self.cancel_label:
                btn = parent.addButton(self.cancel_label, QtGui.QMessageBox.RejectRole)
            else:
                btn = parent.addButton(QtGui.QMessageBox.Cancel)

            if self.default == CANCEL:
                parent.setDefaultButton(btn)

        return None

    def _tk_dialog_assemble(self, dialog, dialog_area, buttons):
        """ Complete the dialog by assembling the various components. """

        if self.size != (-1, -1):
            dialog.resize(*self.size)
