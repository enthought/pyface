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
from enthought.pyface.api import OK, CANCEL, YES, NO


RESULT_MAP = {
    QtGui.QDialog.Accepted:     OK,
    QtGui.QDialog.Rejected:     CANCEL,
    QtGui.QMessageBox.Ok:       OK,
    QtGui.QMessageBox.Cancel:   CANCEL,
    QtGui.QMessageBox.Yes:      YES,
    QtGui.QMessageBox.No:       NO
}

    
class Dialog_qt4(object):
    """ The Dialog monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create the toolkit-specific control that represents the window. """

        # ZZZ: Note that we ignore the resizeable trait at the moment.
        return QtGui.QDialog(parent)

    ###########################################################################
    # 'Window' toolkit interface.
    ###########################################################################

    def _tk_window_add_event_listeners(self, control):
        """ Adds any event listeners required by the window. """

        pass

    ###########################################################################
    # 'Dialog' toolkit interface.
    ###########################################################################

    def _tk_dialog_show_modal(self):
        """ Show a modal dialog and return the pyface result. """

        return RESULT_MAP[self.control.exec_()]

    def _tk_dialog_create_area(self, parent):
        """ Creates the main content of the dialog. """

        panel = QtGui.QWidget(parent)
        panel.resize(100, 200)

        pal = panel.palette()
        pal.setColor(QtGui.QPalette.Window, QtCore.Qt.red)
        panel.setPalette(pal)
        panel.setAutoFillBackground(True)

        return panel

    def _tk_dialog_create_buttons(self, parent):
        """ Creates the buttons. """

        buttons = QtGui.QDialogButtonBox()

        # 'OK' button.
        # ZZZ: Review how this is supposed to work for nonmodal dialogs.
        if self.ok_button_label:
            btn = buttons.addButton(self.ok_button_label, QtGui.QDialogButtonBox.AcceptRole)
        else:
            btn = buttons.addButton(QtGui.QDialogButtonBox.Ok)

        btn.setDefault(True)

        # 'Cancel' button.
        # ZZZ: Review how this is supposed to work for nonmodal dialogs.
        if self.cancel_button_label:
            buttons.addButton(self.cancel_button_label, QtGui.QDialogButtonBox.RejectRole)
        else:
            buttons.addButton(QtGui.QDialogButtonBox.Cancel)

        # 'Help' button.
        # ZZZ: In the original code the only possible hook into the help was to
        # reimplement self._on_help().  However this was a private method.
        # Obviously nobody uses the Help button.  For the moment we display it
        # but can't actually use it.
        if len(self.help_id) > 0:
            if self.help_button_label:
                buttons.addButton(self.help_button_label, QtGui.QDialogButtonBox.HelpRole)
            else:
                buttons.addButton(QtGui.QDialogButtonBox.Help)

        return buttons

    def _tk_dialog_assemble(self, dialog, dialog_area, buttons):
        """ Complete the dialog by assembling the various components. """

        lay = QtGui.QVBoxLayout()

        # Note that we ignore dialog_area_border as this should be defined by
        # the style rather than (non-portable) application code.
        lay.addWidget(dialog_area)
        lay.addWidget(buttons)

        dialog.setLayout(lay)

        if self.size != (-1, -1):
            dialog.resize(*self.size)
