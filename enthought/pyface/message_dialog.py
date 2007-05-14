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
""" A dialog that displays a message. """


# Enthought library imports.
from enthought.traits.api import Enum, Str

# Local imports.
from dialog import Dialog


# Convenience functions.
def information(parent, message, title='Information'):
    """ Convenience function to show an information message dialog. """

    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='information'
    )
    dialog.open()

    return

def warning(parent, message, title='Warning'):
    """ Convenience function to show a warning message dialog. """

    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='warning'
    )
    dialog.open()

    return

def error(parent, message, title='Error'):
    """ Convenience function to show an error message dialog. """

    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='error'
    )
    dialog.open()

    return


class MessageDialog(Dialog):
    """ A dialog that displays a message. """

    __tko__ = 'MessageDialog'

    #### 'Dialog' interface ###################################################

    # Is the dialog resizeable?
    resizeable = False

    #### 'MessageDialog' interface ############################################
    
    # The message to display in the dialog.
    message = Str
    
    # The severity of the message.
    severity = Enum('information', 'warning', 'error')

    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Creates the window contents. """

        # The toolkit is expected to create the whole thing when it creates the
        # control.
        return None

#### EOF ######################################################################
