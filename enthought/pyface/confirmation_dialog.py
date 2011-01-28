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
""" The implementation of a dialog that prompts the user for confirmation. """


# Local imports.
from constant import NO


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


# Import the toolkit specific version.
from toolkit import toolkit_object
ConfirmationDialog = toolkit_object('confirmation_dialog:ConfirmationDialog')

#### EOF ######################################################################
