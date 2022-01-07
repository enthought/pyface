# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The time field interface. """

from datetime import time

from traits.api import HasTraits, Time

from pyface.fields.i_field import IField


class ITimeField(IField):
    """ The time field interface.

    This is for a field that edits a datetime.time value.
    """

    #: The current value of the time field
    value = Time()


class MTimeField(HasTraits):
    """ Mixin class for TimeField implementations """

    #: The current value of the time field
    value = Time()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        super(MTimeField, self)._initialize_control()
        self._set_control_value(self.value)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(MTimeField, self)._add_event_listeners()
        if self.control is not None:
            self._observe_control_value()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            self._observe_control_value(remove=True)
        super(MTimeField, self)._remove_event_listeners()

    # Trait defaults --------------------------------------------------------

    def _value_default(self):
        return time.now()
