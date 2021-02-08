# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The spin field interface. """


from traits.api import HasTraits, Int, Property, Range, Tuple

from pyface.fields.i_field import IField


class ISpinField(IField):
    """ The spin field interface.

    This is for spinners holding integer values.
    """

    #: The current value of the spinner
    value = Range(low="minimum", high="maximum")

    #: The bounds of the spinner
    bounds = Tuple(Int, Int)

    #: The minimum value
    minimum = Property(Int, observe="bounds")

    #: The maximum value
    maximum = Property(Int, observe="bounds")


class MSpinField(HasTraits):

    #: The current value of the spinner
    value = Range(low="minimum", high="maximum")

    #: The bounds for the spinner
    bounds = Tuple(Int, Int)

    #: The minimum value for the spinner
    minimum = Property(Int, observe="bounds")

    #: The maximum value for the spinner
    maximum = Property(Int, observe="bounds")

    # ------------------------------------------------------------------------
    # object interface
    # ------------------------------------------------------------------------

    def __init__(self, **traits):
        value = traits.pop("value", None)
        if "bounds" in traits:
            traits["value"] = traits["bounds"][0]
        super(MSpinField, self).__init__(**traits)
        if value is not None:
            self.value = value

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        super(MSpinField, self)._initialize_control()
        self._set_control_bounds(self.bounds)
        self._set_control_value(self.value)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(MSpinField, self)._add_event_listeners()
        self.observe(self._bounds_updated, "bounds", dispatch="ui")
        if self.control is not None:
            self._observe_control_value()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            self._observe_control_value(remove=True)
        self.observe(
            self._bounds_updated, "bounds", dispatch="ui", remove=True
        )
        super(MSpinField, self)._remove_event_listeners()

    # Toolkit control interface ---------------------------------------------

    def _get_control_bounds(self):
        """ Toolkit specific method to get the control's bounds. """
        raise NotImplementedError()

    def _set_control_bounds(self, bounds):
        """ Toolkit specific method to set the control's bounds. """
        raise NotImplementedError()

    # Trait property handlers -----------------------------------------------

    def _get_minimum(self):
        return self.bounds[0]

    def _set_minimum(self, value):
        if value > self.maximum:
            self.bounds = (value, value)
        else:
            self.bounds = (value, self.maximum)
        if value > self.value:
            self.value = value

    def _get_maximum(self):
        return self.bounds[1]

    def _set_maximum(self, value):
        if value < self.minimum:
            self.bounds = (value, value)
        else:
            self.bounds = (self.minimum, value)
        if value < self.value:
            self.value = value

    # Trait defaults --------------------------------------------------------

    def _value_default(self):
        return self.bounds[0]

    # Trait change handlers --------------------------------------------------

    def _bounds_updated(self, event):
        if self.control is not None:
            self._set_control_bounds(self.bounds)
