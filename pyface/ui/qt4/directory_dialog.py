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
from traits.api import Bool, provides, Unicode

# Local imports.
from pyface.i_directory_dialog import IDirectoryDialog, MDirectoryDialog
from .dialog import Dialog
import six


@provides(IDirectoryDialog)
class DirectoryDialog(MDirectoryDialog, Dialog):
    """ The toolkit specific implementation of a DirectoryDialog.  See the
    IDirectoryDialog interface for the API documentation.
    """


    #### 'IDirectoryDialog' interface #########################################

    default_path = Unicode

    message = Unicode

    new_directory = Bool(True)

    path = Unicode

    ###########################################################################
    # Protected 'IDialog' interface.
    ###########################################################################

    def _create_contents(self, parent):
        # In PyQt this is a canned dialog.
        pass

    ###########################################################################
    # 'IWindow' interface.
    ###########################################################################

    def close(self):
        # Get the path of the chosen directory.
        files = self.control.selectedFiles()

        if files:
            self.path = six.text_type(files[0])
        else:
            self.path = ''

        # Let the window close as normal.
        super(DirectoryDialog, self).close()

    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create_control(self, parent):
        dlg = QtGui.QFileDialog(parent, self.title, self.default_path)

        dlg.setViewMode(QtGui.QFileDialog.Detail)
        dlg.setFileMode(QtGui.QFileDialog.DirectoryOnly)

        if not self.new_directory:
            dlg.setOptions(QtGui.QFileDialog.ReadOnly)

        if self.message:
            dlg.setLabelText(QtGui.QFileDialog.LookIn, self.message)

        return dlg

#### EOF ######################################################################
