# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The field interface. """


from traits.api import Any, HasTraits

from pyface.i_layout_widget import ILayoutWidget


class IField(ILayoutWidget):
    """ The field interface.

    A field is a widget that displays a value and (potentially) allows a user
    to interact with it.
    """

    #: The value held by the field.
    value = Any()


class MField(HasTraits):
    """ The field mix-in. """

    #: The value held by the field.
    value = Any()

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super()._add_event_listeners()
        self.observe(self._value_updated, "value", dispatch="ui")

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        self.observe(
            self._value_updated, "value", dispatch="ui", remove=True
        )
        super()._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _create(self):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        super()._create()

        self.show(self.visible)
        self.enable(self.enabled)

    def _update_value(self, value):
        """ Handle a change to the value from user interaction

        This is a method suitable for calling from a toolkit event handler.
        """
        self.value = self._get_control_value()

    def _get_control(self):
        """ If control is not passed directly, get it from the trait. """
        control = self.control
        if control is None:
            raise RuntimeError("Toolkit control does not exist.")
        return control

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        raise NotImplementedError()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        raise NotImplementedError()

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        raise NotImplementedError()

    # Trait change handlers -------------------------------------------------

    def _value_updated(self, event):
        value = event.new
        if self.control is not None:
            self._set_control_value(value)
