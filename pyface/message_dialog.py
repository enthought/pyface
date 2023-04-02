# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The implementation of a dialog that displays a message. """


# Import the toolkit specific version.
from .toolkit import toolkit_object


MessageDialog = toolkit_object("message_dialog:MessageDialog")


# Convenience functions.
def information(
    parent,
    message,
    title="Information",
    detail="",
    informative="",
    text_format="auto"
):
    """ Convenience method to show an information message dialog.

    Parameters
    ----------
    parent : toolkit control or None
        The toolkit control that should be the parent of the dialog.
    message : str
        The text of the message to display.
    title : str
        The text of the dialog title.
    detail : str
        Further details about the message (displayed when the user clicks
        "Show details").
    informative : str
        Explanatory text to display along with the message.
    text_format : str
        Specifies what text format to use in the resulting message dialog.
        One of "auto", "plain", or "rich". Only supported on the qt backend.

    """
    dialog = MessageDialog(
        parent=parent,
        message=message,
        title=title,
        severity="information",
        detail=detail,
        informative=informative,
        text_format=text_format,
    )
    dialog.open()


def warning(
    parent,
    message,
    title="Warning",
    detail="",
    informative="",
    text_format="auto"
):
    """ Convenience function to show a warning message dialog.

    Parameters
    ----------
    parent : toolkit control or None
        The toolkit control that should be the parent of the dialog.
    message : str
        The text of the message to display.
    title : str
        The text of the dialog title.
    detail : str
        Further details about the message (displayed when the user clicks
        "Show details").
    informative : str
        Explanatory text to display along with the message.
    text_format : str
        Specifies what text format to use in the resulting message dialog.
        One of "auto", "plain", or "rich". Only supported on the qt backend.

    """
    dialog = MessageDialog(
        parent=parent,
        message=message,
        title=title,
        severity="warning",
        detail=detail,
        informative=informative,
        text_format=text_format,
    )
    dialog.open()


def error(
    parent,
    message,
    title="Error",
    detail="",
    informative="",
    text_format="auto"
):
    """ Convenience function to show an error message dialog.

    Parameters
    ----------
    parent : toolkit control or None
        The toolkit control that should be the parent of the dialog.
    message : str
        The text of the message to display.
    title : str
        The text of the dialog title.
    detail : str
        Further details about the message (displayed when the user clicks
        "Show details").
    informative : str
        Explanatory text to display along with the message.
    text_format : str
        Specifies what text format to use in the resulting message dialog.
        One of "auto", "plain", or "rich". Only supported on the qt backend.

    """
    dialog = MessageDialog(
        parent=parent,
        message=message,
        title=title,
        severity="error",
        detail=detail,
        informative=informative,
        text_format=text_format,
    )
    dialog.open()
