#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class DirectoryDialog_qt4(object):
    """ The DirectoryDialog monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create the toolkit specific control that represents the dialog. """

        dialog = QtGui.QFileDialog(parent, self.title, self.default_path)
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)

        if not self.new_directory:
            dialog.setReadOnly(True)

        if self.message:
            dialog.setLabelText(QtGui.QFileDialog.LookIn, self.message)

        return dialog

    ###########################################################################
    # 'DirectoryDialog' toolkit interface.
    ###########################################################################

    def _tk_directorydialog_get_path(self):
        """ Return the selected pathname. """

        files = self.control.selectedFiles()

        if files:
            file = str(files[0])
        else:
            file = ''

        return file
