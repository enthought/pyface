# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for a dialog that prompts the user for confirmation. """


from traits.api import Bool, Enum, HasTraits, Str


from pyface.constant import CANCEL, NO, YES
from pyface.i_dialog import IDialog
from pyface.ui_traits import Image


class IConfirmationDialog(IDialog):
    """ The interface for a dialog that prompts the user for confirmation. """

    # 'IConfirmationDialog' interface -------------------------------------#

    #: Should the cancel button be displayed?
    cancel = Bool(False)

    #: The default button.
    default = Enum(NO, YES, CANCEL)

    #: The image displayed with the message.  The default is toolkit specific.
    image = Image()

    #: The message displayed in the body of the dialog (use the inherited
    #: 'title' trait to set the title of the dialog itself).
    message = Str()

    #: Some informative text to display below the main message
    informative = Str()

    #: Some additional details that can be exposed by the user
    detail = Str()

    #: The label for the 'no' button.  The default is toolkit specific.
    no_label = Str()

    #: The label for the 'yes' button.  The default is toolkit specific.
    yes_label = Str()


class MConfirmationDialog(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IConfirmationDialog interface.
    """
