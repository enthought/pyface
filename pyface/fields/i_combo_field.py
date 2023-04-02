# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The combo field interface. """


from traits.api import Callable, HasTraits, Enum, List

from pyface.fields.i_editable_field import IEditableField


class IComboField(IEditableField):
    """ The combo field interface.

    This is for comboboxes holding a list of values.
    """

    #: The current value of the combobox.
    value = Enum(values="values")

    #: The list of available values for the combobox.
    values = List()

    #: Callable that converts a value to text plus an optional icon.
    #: Should return either a uncode string or a tuple of image resource
    #: and string.
    formatter = Callable(str, allow_none=False)


class MComboField(HasTraits):

    #: The current text value of the combobox.
    value = Enum(values="values")

    #: The list of available values for the combobox.
    values = List(minlen=1)

    #: Callable that converts a value to text plus an optional icon.
    #: Should return either a uncode string or a tuple of image resource
    #: and string.
    formatter = Callable(str, allow_none=False)

    # ------------------------------------------------------------------------
    # object interface
    # ------------------------------------------------------------------------

    def __init__(self, values, **traits):
        value = traits.pop("value", values[0])
        traits["values"] = values
        super().__init__(**traits)
        self.value = value

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        super()._initialize_control()
        self._set_control_values(self.values)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super()._add_event_listeners()
        self.observe(
            self._values_updated, "values.items,formatter", dispatch="ui"
        )

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        self.observe(
            self._values_updated,
            "values.items,formatter",
            dispatch="ui",
            remove=True,
        )
        super()._remove_event_listeners()

    # Toolkit control interface ---------------------------------------------

    def _get_control_text_values(self):
        """ Toolkit specific method to get the control's text values. """
        raise NotImplementedError()

    def _set_control_values(self, values):
        """ Toolkit specific method to set the control's values. """
        raise NotImplementedError()

    # Trait change handlers --------------------------------------------------

    def _values_updated(self, event):
        if self.control is not None:
            self._set_control_values(self.values)
