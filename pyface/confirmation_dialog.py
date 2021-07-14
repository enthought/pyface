# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The implementation of a dialog that prompts the user for confirmation. """


from .constant import NO


def confirm(parent, message, title=None, cancel=False, default=NO):
    """ Convenience method to show a confirmation dialog.

    Parameters
    ----------
    parent : toolkit widget or None
        The parent control for the dialog.
    message : str
        The text of the message to display.
    title : str
        The text of the dialog title.
    cancel : bool
        ``True`` if the dialog should contain a Cancel button.
    default : NO, YES or CANCEL
        Which button should be the default button.
    """
    if title is None:
        title = "Confirmation"

    dialog = ConfirmationDialog(
        parent=parent,
        message=message,
        cancel=cancel,
        default=default,
        title=title,
    )

    return dialog.open()


# Import the toolkit specific version.
from .toolkit import toolkit_object

ConfirmationDialog = toolkit_object("confirmation_dialog:ConfirmationDialog")
