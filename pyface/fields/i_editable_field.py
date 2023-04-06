# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The editable field interface. """


from traits.api import HasTraits

from .i_field import IField


class IEditableField(IField):
    """ The editable field interface.

    A editable field is a widget that displays a user-editable value.
    """


class MEditableField(HasTraits):
    """The editable field mix-in.

    Classes which use this mixin should implement _observe_control_value to
    connect a toolkit handler that calls _update_value.
    """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super()._add_event_listeners()
        self._observe_control_value()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        self._observe_control_value(remove=True)
        super()._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _update_value(self, value):
        """ Handle a change to the value from user interaction

        This is a method suitable for calling from a toolkit event handler.
        """
        self.value = self._get_control_value()

    # Toolkit control interface ---------------------------------------------

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        raise NotImplementedError()
