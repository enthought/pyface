# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for a dialog that displays a message. """


from traits.api import Enum, HasTraits, Str


from pyface.i_dialog import IDialog


class IMessageDialog(IDialog):
    """ The interface for a dialog that displays a message. """

    # 'IMessageDialog' interface -------------------------------------------

    #: The message to display in the dialog.
    message = Str()

    #: More information about the message to be displayed.
    informative = Str()

    #: More detail about the message to be displayed in the dialog.
    detail = Str()

    #: The severity of the message.
    severity = Enum("information", "warning", "error")


class MMessageDialog(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IMessageDialog interface.
    """
