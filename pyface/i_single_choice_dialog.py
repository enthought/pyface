# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for a dialog that prompts for a choice from a list. """


from traits.api import Any, HasTraits, List, Str


from pyface.i_dialog import IDialog


class ISingleChoiceDialog(IDialog):
    """ The interface for a dialog that prompts for a choice from a list. """

    # 'ISingleChoiceDialog' interface -------------------------------------#

    #: List of objects to choose from.
    choices = List(Any)

    #: The object chosen, if any.
    choice = Any()

    #: An optional attribute to use for the name of each object in the dialog.
    name_attribute = Str()

    #: The message to display to the user.
    message = Str()


class MSingleChoiceDialog(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IConfirmationDialog interface.
    """

    def _choice_strings(self):
        """ Returns the list of strings to display in the dialog. """
        choices = self.choices
        if self.name_attribute != "":
            # choices is a list of objects with this attribute
            choices = [getattr(obj, self.name_attribute) for obj in choices]

        choices = [str(obj) for obj in choices]

        if len(choices) == 0:
            raise ValueError("SingleChoiceDialog requires at least 1 choice.")
        elif len(choices) != len(set(choices)):
            raise ValueError(
                "Dialog choices {} contain repeated string value." % choices
            )
        return choices
