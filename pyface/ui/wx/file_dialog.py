# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
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


import os


import wx


from traits.api import Enum, Int, List, provides, Str


from pyface.i_file_dialog import IFileDialog, MFileDialog
from .dialog import Dialog


@provides(IFileDialog)
class FileDialog(MFileDialog, Dialog):
    """ The toolkit specific implementation of a FileDialog.  See the
    IFileDialog interface for the API documentation.
    """

    # 'IFileDialog' interface ---------------------------------------------#

    action = Enum("open", "open files", "save as")

    default_directory = Str()

    default_filename = Str()

    default_path = Str()

    directory = Str()

    filename = Str()

    path = Str()

    paths = List(Str)

    wildcard = Str()

    wildcard_index = Int(0)

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
        # Work around wx bug throwing exception on cancel of file dialog
        if len(self.path) > 0:
            self.paths = self.control.GetPaths()
        else:
            self.paths = []

        # Extract the directory and filename.
        self.directory, self.filename = os.path.split(self.path)

        # Get the index of the selected filter.
        self.wildcard_index = self.control.GetFilterIndex()
        # Let the window close as normal.
        super().close()

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        # If the caller provided a default path instead of a default directory
        # and filename, split the path into it directory and filename
        # components.
        if (
            len(self.default_path) != 0
            and len(self.default_directory) == 0
            and len(self.default_filename) == 0
        ):
            default_directory, default_filename = os.path.split(
                self.default_path
            )
        else:
            default_directory = self.default_directory
            default_filename = self.default_filename

        if self.action == "open":
            style = wx.FD_OPEN
        elif self.action == "open files":
            style = wx.FD_OPEN | wx.FD_MULTIPLE
        else:
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT

        # Create the actual dialog.
        dialog = wx.FileDialog(
            parent,
            self.title,
            defaultDir=default_directory,
            defaultFile=default_filename,
            style=style,
            wildcard=self.wildcard.rstrip("|"),
        )

        dialog.SetFilterIndex(self.wildcard_index)

        return dialog

    # ------------------------------------------------------------------------
    # Trait handlers.
    # ------------------------------------------------------------------------

    def _wildcard_default(self):
        """ Return the default wildcard. """

        return self.WILDCARD_ALL
