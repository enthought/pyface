# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The toggle field interface. """


from traits.api import Bool, HasTraits, Str

from pyface.fields.i_editable_field import IEditableField
from pyface.ui_traits import Image


class IToggleField(IEditableField):
    """ The toggle field interface.

    This is for a toggle between two states, represented by a boolean value.
    """

    #: The current value of the toggle.
    value = Bool()

    #: The text to display in the toggle.
    text = Str()

    #: The icon to display with the toggle.
    icon = Image()


class MToggleField(HasTraits):
    """ The toggle field mixin class.

    This is for a toggle between two states, represented by a boolean value.
    """

    #: The current value of the toggle.
    value = Bool()

    #: The text to display in the toggle.
    text = Str()

    #: The icon to display with the toggle.
    icon = Image()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        super()._initialize_control()
        self._set_control_text(self.text)
        self._set_control_icon(self.icon)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super()._add_event_listeners()
        self.observe(self._text_updated, "text", dispatch="ui")
        self.observe(self._icon_updated, "icon", dispatch="ui")

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        self.observe(self._text_updated, "text", dispatch="ui", remove=True)
        self.observe(self._icon_updated, "icon", dispatch="ui", remove=True)
        super()._remove_event_listeners()

    # Toolkit control interface ---------------------------------------------

    def _get_control_text(self):
        """ Toolkit specific method to set the control's text. """
        raise NotImplementedError()

    def _set_control_text(self, text):
        """ Toolkit specific method to set the control's text. """
        raise NotImplementedError()

    def _set_control_icon(self, icon):
        """ Toolkit specific method to set the control's icon. """
        raise NotImplementedError()

    # Trait change handlers -------------------------------------------------

    def _text_updated(self, event):
        if self.control is not None:
            self._set_control_text(self.text)

    def _icon_updated(self, event):
        if self.control is not None:
            self._set_control_icon(self.icon)
