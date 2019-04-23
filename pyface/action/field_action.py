# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from traits.api import Any, Constant, Dict, Str, Type

from pyface.fields.i_field import IField
from .action import Action
from .action_event import ActionEvent


class FieldAction(Action):
    """ A widget action containing an IField

    When the value in the field is changed, the `on_peform` method is called
    with the new value as the argument.
    """

    #: This is a widget action.
    style = Constant("widget")

    #: The field to display.
    field_type = Type(IField)

    #: The default trait values for the field.
    field_defaults = Dict(Str, Any)

    def create_control(self, parent):
        """ Called when creating a "widget" style action.

        This constructs an IField-based control directly and binds changes to
        the value to the `value_updated` method.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control, usually a toolbar.

        Returns
        -------
        control : toolkit control
            A toolkit control or None.
        """
        field = self.field_type(parent=parent, **self.field_defaults)
        field._create()
        field.on_trait_change(self.value_updated, 'value')
        field.control._field = field
        return field.control

    def value_updated(self, value):
        """ Handle changes to the field value by calling perform.

        The event passed to `perform` has the `value` as an attribute.
        """
        action_event = ActionEvent(value=value)
        self.perform(action_event)

    def perform(self, event):
        """ Performs the action.

        This dispacthes to the on_perform method with the new value passed
        as an argument.

        Parameters
        ----------
        event : ActionEvent instance
            The event which triggered the action.
        """
        if self.on_perform is not None:
            self.on_perform(event.value)
