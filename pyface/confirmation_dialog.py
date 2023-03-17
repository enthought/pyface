# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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
from .toolkit import toolkit_object


ConfirmationDialog = toolkit_object("confirmation_dialog:ConfirmationDialog")


def confirm(
    parent,
    message,
    title=None,
    cancel=False,
    default=NO,
    no_label="",
    yes_label="",
    informative="",
    detail="",
):
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
    no_label : str
        Text to display in the NO button.
    yes_label : str
        Text to display in the YES button.
    informative : str
        Explanatory text to display along with the message.
    detail : str
        Further details about the message (displayed when the user clicks
        "Show details").
    """
    if title is None:
        title = "Confirmation"

    dialog = ConfirmationDialog(
        parent=parent,
        message=message,
        cancel=cancel,
        default=default,
        no_label=no_label,
        yes_label=yes_label,
        title=title,
        informative=informative,
        detail=detail,
    )

    return dialog.open()
