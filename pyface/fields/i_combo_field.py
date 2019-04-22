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

from traits.api import Callable, HasTraits, Enum, List

from pyface.fields.i_field import IField


class IComboField(IField):
    """ The combo field interface.

    This is for comboboxes holding a list of values.
    """

    #: The current value of the combobox.
    value = Enum(values='values')

    #: The list of available values for the combobox.
    values = List

    #: Callable that converts a value to text plus an optional icon.
    #: Should return either a uncode string or a tuple of image resource
    #: and string.
    formatter = Callable(text_type, allow_none=False)


class MComboField(HasTraits):

    #: The current text value of the combobox.
    value = Enum(values='values')

    #: The list of available values for the combobox.
    values = List(minlen=1)

    #: Callable that converts a value to text plus an optional icon.
    #: Should return either a uncode string or a tuple of image resource
    #: and string.
    formatter = Callable(text_type, allow_none=False)

    # ------------------------------------------------------------------------
    # object interface
    # ------------------------------------------------------------------------

    def __init__(self, values, **traits):
        value = traits.pop('value', values[0])
        traits['values'] = values
        super(MComboField, self).__init__(**traits)
        self.value = value

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        super(MComboField, self)._initialize_control()
        self._set_control_values(self.values)
        self._set_control_value(self.value)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(MComboField, self)._add_event_listeners()
        self.on_trait_change(self._values_updated, 'values[],formatter',
                             dispatch='ui')
        if self.control is not None:
            self._observe_control_value()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            self._observe_control_value(remove=True)
        self.on_trait_change(self._values_updated, 'values[],formatter',
                             dispatch='ui', remove=True)
        super(MComboField, self)._remove_event_listeners()

    # Toolkit control interface ---------------------------------------------

    def _get_control_text_values(self):
        """ Toolkit specific method to get the control's text values. """
        raise NotImplementedError

    def _set_control_values(self, values):
        """ Toolkit specific method to set the control's values. """
        raise NotImplementedError

    # Trait change handlers --------------------------------------------------

    def _values_updated(self):
        if self.control is not None:
            self._set_control_values(self.values)
