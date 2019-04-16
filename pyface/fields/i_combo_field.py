#------------------------------------------------------------------------------
# Copyright (c) 2019, Enthought, Inc.
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

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from six import text_type

from traits.api import (
    Bool, Callable, HasTraits, Enum, List, Unicode, on_trait_change
)

from pyface.fields.i_field import IField


class IComboField(IField):
    """ The combo field interface.

    This is for comboboxes holding a list of values.
    """

    #: The current value of the combobox.
    value = Enum(values='values')

    #: The list of available values for the combobox.
    values = List

    #: Whether the text is editable.  This should not be changed after the
    #: control is created.
    editable = Bool

    #: The current contents of the text field.
    edit_text = Unicode

    #: Callable that converts a value to text plus an optional icon.
    #: Should return either a uncode string or a tuple of image resource
    #: and string.
    formatter = Callable(text_type, allow_none=False)


class MComboField(HasTraits):

    #: The current text value of the combobox.
    value = Enum(None, values='values')

    #: The list of available values for the combobox.
    values = List

    #: Whether the text is editable.  This should not be changed after the
    #: control is created.
    editable = Bool

    #: The current contents of the text field.
    edit_text = Unicode

    #: Callable that converts a value to text plus an optional icon.
    #: Should return either a uncode string or a tuple of image resource
    #: and string.
    formatter = Callable(text_type, allow_none=False)

    def _populate_values(self, control=None):
        raise NotImplementedError()

    def _update_value(self, control, value):
        raise NotImplementedError()

    # Trait change handlers --------------------------------------------------

    def _value_changed(self, value):
        if self.control is not None:
            self._update_value(self.control, value)

    @on_trait_change('values[]')
    def _values_changed(self, new):
        if self.control is not None:
            self._populate_values()

    def _editable_changed(self):
        if self.control is not None:
            raise RuntimeError(
                "Editable state of ComboField cannot be changed while "
                "control is live."
            )
