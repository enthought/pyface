# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The implementation of a dialog that allows the user to select a font.
"""

from .constant import OK
from .toolkit import toolkit_object


FontDialog = toolkit_object("font_dialog:FontDialog")


def get_font(parent, font):
    """ Convenience function that displays a font dialog.

    Parameters
    ----------
    parent : toolkit control
        The parent toolkit control for the modal dialog.
    font : Font or font description
        The initial Font object or string describing the font.

    Returns
    -------
    font : Font or None
        The selected font, or None if the user made no selection.
    """
    dialog = FontDialog(parent=parent, font=font)
    result = dialog.open()
    if result == OK:
        return dialog.font
    else:
        return None
