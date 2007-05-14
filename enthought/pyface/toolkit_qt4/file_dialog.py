#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


class FileDialog_qt4(object):
    """ The FileDialog monkey patch for Qt4. """

    ###########################################################################
    # 'FileDialog' toolkit interface.
    ###########################################################################

    def _tk_filedialog_create(self, parent, directory, filename):
        """ Create the toolkit specific control that represents the dialog. """

        # Convert the filter.
        keep = True
        filters = QtCore.QStringList()

        for f in self.wildcard.split('|'):
            if keep and f:
                filters << f

            keep = not keep

        # The default directory for wx is the current one, so do the same.
        if not directory:
            directory = QtCore.QDir.currentPath()

        dialog = QtGui.QFileDialog(parent, self.title, directory)
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        dialog.selectFile(filename)
        dialog.setFilters(filters)

        if self.action == 'open':
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
            dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        else:
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
            dialog.setFileMode(QtGui.QFileDialog.AnyFile)

        return dialog

    def _tk_filedialog_get_path(self):
        """ Return the selected pathname. """

        files = self.control.selectedFiles()

        if files:
            file = str(files[0])
        else:
            file = ''

        return file
