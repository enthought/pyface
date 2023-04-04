# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A dialog that allows the user to chose a single item from a list. """


from .constant import OK
from .toolkit import toolkit_object


# Import the toolkit specific version.
SingleChoiceDialog = toolkit_object("single_choice_dialog:SingleChoiceDialog")


# Convenience functions.
def choose_one(parent, message, choices, title="Choose", cancel=True):
    """ Convenience method to show an information message dialog.

    Parameters
    ----------
    parent : toolkit control or None
        The toolkit control that should be the parent of the dialog.
    message : str
        The text of the message to display.
    choices : list
        List of objects to choose from.
    title : str
        The text of the dialog title.
    cancel : bool
        Whether or not the dialog can be cancelled.

    Returns
    -------
    choice : Any
        The selected object, or None if cancelled.
    """
    dialog = SingleChoiceDialog(
        parent=parent,
        message=message,
        choices=choices,
        title=title,
        cancel=cancel,
    )
    result = dialog.open()
    if result == OK:
        choice = dialog.choice
    else:
        choice = None
    return choice
