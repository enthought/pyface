#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" A dialog that allows the user to open/save files etc. """


# Standard library imports.
import os
import sys

# Enthought library imports.
from enthought.traits.api import Enum, Str

# Local imports.
from dialog import Dialog


# The conventional globbing scheme for "all files" is platform-specific.
if sys.platform == 'win32':
    _wildcard_all = "All files (*.*)|*.*|"
else:
    _wildcard_all = "All files (*)|*"


class FileDialog(Dialog):
    """ A dialog that allows the user to open/save files etc. """

    __tko__ = 'FileDialog'

    # FIXME v3: These are referenced elsewhere so maybe should be part of the
    # interface. The format is toolkit specific and so shouldn't be exposed.
    # The create_wildcard() class method (why isn't it a static method?) should
    # be the basis for this - but nothing seems to use it.  For now the PyQt
    # implementation will convert the wx format to its own.

    # A file dialog wildcard for Python files.
    WILDCARD_PY = "Python files (*.py)|*.py|"

    # A file dialog wildcard for text files.
    WILDCARD_TXT = "Text files (*.txt)|*.txt|"

    # A file dialog wildcard for all files.
    WILDCARD_ALL = _wildcard_all

    # A file dialog wildcard for Zip archives.
    WILDCARD_ZIP = "Zip files (*.zip)|*.zip|"

    #### 'FileDialog' interface ###############################################

    # The 'action' that the user is peforming on the directory.
    action = Enum('open', 'save as')

    # The default directory.
    default_directory = Str

    # The default filename.
    default_filename = Str

    # The default path (directory and filename) of the chosen file.  This is
    # only used when the *default_directory* and *default_filename* are not
    # set and is equivalent to setting both.
    default_path = Str

    # The directory containing the chosen file.
    directory = Str

    # The name of the chosen file.
    filename = Str

    # The path (directory and filename) of the chosen file.
    path = Str

    # The wildcard used to restrict the set of files.
    wildcard = Str(WILDCARD_ALL)

    ###########################################################################
    # 'FileDialog' interface.
    ###########################################################################

    def create_wildcard(cls, description, extension):
        """ Creates a wildcard for a given extension.

        e.g. FileDialog.create_wildcard('Python files', '*.py')

             or

             FileDialog.create_wildcard('HTML Files', ['*.htm', '*.html'])

        """

        if isinstance(extension, basestring):
            pattern = extension

        else:
            pattern = ';'.join(extension)

        return "%s (%s)|%s|" % (description, pattern, pattern)

    create_wildcard = classmethod(create_wildcard)

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def close(self):
        """ Closes the window. """

        # Get the path of the chosen directory.
        self.path = self._tk_filedialog_get_path()

        # Extract the directory and filename.
        self.directory, self.filename = os.path.split(self.path)

        # Let the window close as normal.
        super(FileDialog, self).close()

        return

    ###########################################################################
    # Protected 'Widget' interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Create the toolkit specific control that represents the window. """

        # If the caller provided a default path instead of a default directory
        # and filename, split the path into it directory and filename
        # components.
        if len(self.default_path) > 0 and len(self.default_directory) < 1 \
            and len(self.default_filename) < 1:
            default_directory, default_filename = os.path.split(
                self.default_path)
        else:
            default_directory = self.default_directory
            default_filename = self.default_filename

        return self._tk_filedialog_create(parent, default_directory, default_filename)

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # The toolkit is expected to create the whole thing when it creates the
        # control.
        return None

    ###########################################################################
    # 'FileDialog' toolkit interface.
    ###########################################################################

    def _tk_filedialog_create(self, parent, directory, filename):
        """ Create the toolkit specific control that represents the dialog.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_filedialog_get_path(self):
        """ Return the selected pathname.
        
        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
