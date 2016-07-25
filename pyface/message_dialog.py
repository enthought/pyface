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
""" The implementation of a dialog that displays a message. """

from __future__ import absolute_import


# Convenience functions.
def information(parent, message, title='Information',
                detail='', informative=''):
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

    """
    dialog = MessageDialog(
        parent=parent, message=message, title=title,
        severity='information', detail=detail, informative=informative
    )
    dialog.open()


def warning(parent, message, title='Warning', detail='', informative=''):
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

    """
    dialog = MessageDialog(
        parent=parent, message=message, title=title,
        severity='warning', detail=detail, informative=informative
    )
    dialog.open()


def error(parent, message, title='Error', detail='', informative=''):
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

    """
    dialog = MessageDialog(
        parent=parent, message=message, title=title, severity='error',
        detail=detail, informative=informative
    )
    dialog.open()


# Import the toolkit specific version.
from .toolkit import toolkit_object
MessageDialog = toolkit_object('message_dialog:MessageDialog')

#### EOF ######################################################################
