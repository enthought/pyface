# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""


import wx


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
        # In wx this is a canned dialog.
        pass

    # ------------------------------------------------------------------------
    # 'IWindow' interface.
    # ------------------------------------------------------------------------

    def close(self):
        # Get the path of the chosen directory.
        self.path = str(self.control.GetPath())

        # Let the window close as normal.
        super().close()

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        # The default style.
        style = wx.FD_OPEN

        # Create the wx style depending on which buttons are required etc.
        if self.new_directory:
            style = style | wx.DD_NEW_DIR_BUTTON

        if self.message:
            message = self.message
        else:
            message = "Choose a directory"

        # Create the actual dialog.
        return wx.DirDialog(
            parent, message=message, defaultPath=self.default_path, style=style
        )
