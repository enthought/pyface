# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The label field interface. """


from traits.api import HasTraits, Str

from pyface.fields.i_field import IField
from pyface.ui_traits import Image


class ILabelField(IField):
    """ The label field interface. """

    #: The value held by the field.
    value = Str()

    #: The icon to display with the toggle.
    icon = Image()


class MLabelField(HasTraits):
    """ The text field mix-in. """

    #: The value held by the field.
    value = Str()

    #: The icon to display with the toggle.
    icon = Image()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        super()._initialize_control()
        self._set_control_icon(self.icon)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super()._add_event_listeners()
        self.observe(self._icon_updated, "icon", dispatch="ui")

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        self.observe(self._icon_updated, "icon", dispatch="ui", remove=True)
        super()._remove_event_listeners()

    # Toolkit control interface ---------------------------------------------

    def _set_control_icon(self, icon):
        """ Toolkit specific method to set the control's icon. """
        raise NotImplementedError()

    # Trait change handlers -------------------------------------------------

    def _icon_updated(self, event):
        if self.control is not None:
            self._set_control_icon(self.icon)
