# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


from pyface.qt import QtGui


from traits.api import Bool, provides, Str


from pyface.i_directory_dialog import IDirectoryDialog, MDirectoryDialog
from .dialog import Dialog


@provides(IDirectoryDialog)
class DirectoryDialog(MDirectoryDialog, Dialog):
    """ The toolkit specific implementation of a DirectoryDialog.  See the
    IDirectoryDialog interface for the API documentation.
    """

    # 'IDirectoryDialog' interface -----------------------------------------

    default_path = Str()

    message = Str()

    new_directory = Bool(True)

    path = Str()

    # ------------------------------------------------------------------------
    # Protected 'IDialog' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        # In PyQt this is a canned dialog.
        pass

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def close(self):
        # Get the path of the chosen directory.
        if self.control is not None:
            files = self.control.selectedFiles()
        else:
            files = []

        if files:
            self.path = str(files[0])
        else:
            self.path = ""

        # Let the window close as normal.
        super().close()

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        dlg = QtGui.QFileDialog(parent, self.title, self.default_path)

        dlg.setViewMode(QtGui.QFileDialog.ViewMode.Detail)
        dlg.setFileMode(QtGui.QFileDialog.FileMode.Directory)

        if not self.new_directory:
            dlg.setOptions(QtGui.QFileDialog.Option.ReadOnly)

        if self.message:
            dlg.setLabelText(QtGui.QFileDialog.DialogLabel.LookIn, self.message)

        return dlg
