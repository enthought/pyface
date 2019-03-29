#------------------------------------------------------------------------------
# Copyright (c) 2017-19, Enthought, Inc.
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
""" The text field interface. """

from traits.api import Bool, Callable, Enum, HasTraits, Unicode

from pyface.fields.i_field import IField


class ITextField(IField):
    """ The text field interface. """

    #: The value held by the field.
    value = Unicode

    #: Should the text trait be updated on user edits, or when done editing.
    update_text = Enum('auto', 'editing_finished')

    #: Placeholder text for an empty field.
    placeholder = Unicode

    #: Display typed text, or one of several hidden "password" modes.
    echo = Enum('normal', 'password')

    #: Whether or not the field is read-only.
    read_only = Bool

    def _text_edited(self, text):
        """ Handle a change to the text from user editing

        This is a method suitable for calling from a toolkit event handler.
        """


class MTextField(HasTraits):
    """ The text field mix-in. """
    # this currently does nothing
    pass
