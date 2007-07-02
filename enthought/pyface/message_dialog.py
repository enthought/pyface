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
""" The interface for a dialog that displays a message. """


# Enthought library imports.
from enthought.traits.api import Enum, Unicode

# Local imports.
from dialog import IDialog


# Convenience functions.
def information(parent, message, title='Information'):
    """ Convenience function to show an information message dialog. """

    from enthought.pyface.api import MessageDialog

    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='information'
    )
    dialog.open()

    return

def warning(parent, message, title='Warning'):
    """ Convenience function to show a warning message dialog. """

    from enthought.pyface.api import MessageDialog

    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='warning'
    )
    dialog.open()

    return

def error(parent, message, title='Error'):
    """ Convenience function to show an error message dialog. """

    from enthought.pyface.api import MessageDialog

    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='error'
    )
    dialog.open()

    return


class IMessageDialog(IDialog):
    """ The interface for a dialog that displays a message. """

    #### 'IMessageDialog' interface ###########################################
    
    # The message to display in the dialog.
    message = Unicode
    
    # The severity of the message.
    severity = Enum('information', 'warning', 'error')


class MMessageDialog(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IMessageDialog interface.
    """

#### EOF ######################################################################
