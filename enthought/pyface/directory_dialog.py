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
""" A dialog that allows the user to browse for a directory. """


# Enthought library imports.
from enthought.traits.api import Bool, Str, Trait

# Local imports.
from dialog import Dialog


class DirectoryDialog(Dialog):
    """ A dialog that allows the user to browse for a directory. """

    __tko__ = 'DirectoryDialog'

    #### 'DirectoryDialog' interface ##########################################

    # The 'action' that the user is peforming on the directory.
    #
    # fixme: Support something other than 'open'!
    action = Trait('open', 'open')

    # The default path.
    default_path = Str
    
    # True iff the dialog should include a button that allows the user to
    # create a new directory.
    new_directory = Bool(True)

    # The message to display in the dialog.  The default is toolkit specific.
    message = Str

    # The path of the chosen directory.
    path = Str

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def close(self):
        """ Closes the window. """

        # Get the path of the chosen directory.
        self.path = self._tk_directorydialog_get_path()

        # Let the window close as normal.
        super(DirectoryDialog, self).close()

        return
    
    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # The toolkit is expected to create the whole thing when it creates the
        # control.
        return None

    ###########################################################################
    # 'DirectoryDialog' toolkit interface.
    ###########################################################################

    def _tk_directorydialog_get_path(self):
        """ Return the selected pathname.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
