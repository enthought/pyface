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
""" A dialog that prompts the user for confirmation. """


# Enthought library imports.
from enthought.traits.api import Bool, Enum, Instance, Str

# Local imports.
from constant import CANCEL, NO, YES
from dialog import Dialog
from image_resource import ImageResource


def confirm(parent, message, title=None, cancel=False, default=NO):
    """ Convenience function to show a confirmation dialog. """
    
    if title is None:
        title = "Confirmation"

    dialog = ConfirmationDialog(
        parent  = parent,
        message = message,
        cancel  = cancel,
        default = default,
        title   = title
    )

    return dialog.open()


class ConfirmationDialog(Dialog):
    """ A dialog that prompts the user for confirmation. """

    __tko__ = 'ConfirmationDialog'

    #### 'Dialog' interface ###################################################

    # Is the dialog resizeable?
    resizeable = False

    #### 'ConfirmationDialog' interface #######################################

    # Should the cancel button be displayed?
    cancel = Bool(False)
    
    # The default button.
    default = Enum(NO, YES, CANCEL)
    
    # The image displayed to the left of the message.  The default is toolkit
    # specific.
    image = Instance(ImageResource)

    # The message displayed in the body of the dialog (use the inherited
    # 'title' trait to set the title of the dialog itself).
    message = Str

    # Button labels.  The defaults are toolkit specific.
    yes_label    = Str
    no_label     = Str
    cancel_label = Str

#### EOF ######################################################################
