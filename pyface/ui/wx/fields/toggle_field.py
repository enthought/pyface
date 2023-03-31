# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the toggle field class """

import wx

from traits.api import provides

from pyface.fields.i_toggle_field import IToggleField, MToggleField
from .editable_field import EditableField


@provides(IToggleField)
class ToggleField(MToggleField, EditableField):
    """ The Wx-specific implementation of the toggle field class """

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.GetValue()

    def _get_control_text(self):
        """ Toolkit specific method to get the control's text. """
        return self.control.GetLabel()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.SetValue(value)

    def _set_control_text(self, text):
        """ Toolkit specific method to set the control's text. """
        self.control.SetLabel(text)

    def _set_control_icon(self, icon):
        """ Toolkit specific method to set the control's icon. """
        # don't support icons on Wx for now
        pass


class CheckBoxField(ToggleField):
    """ The Wx-specific implementation of the checkbox class """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = wx.CheckBox(parent)
        return control

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        super()._set_control_value(value)
        event = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, self.control.GetId())
        event.SetInt(value)
        wx.PostEvent(self.control.GetEventHandler(), event)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(wx.EVT_CHECKBOX, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_CHECKBOX, self._update_value)


class RadioButtonField(ToggleField):
    """ The Wx-specific implementation of the radio button class

    This is intended to be used in groups, and shouldn't be used by itself.
    """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = wx.RadioButton(parent)
        return control

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        super()._set_control_value(value)
        event = wx.CommandEvent(wx.EVT_RADIOBUTTON.typeId, self.control.GetId())
        event.SetInt(value)
        wx.PostEvent(self.control.GetEventHandler(), event)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(wx.EVT_RADIOBUTTON, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_RADIOBUTTON, self._update_value)


class ToggleButtonField(ToggleField):
    """ The Wx-specific implementation of the toggle button class """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = wx.ToggleButton(parent)
        return control

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        super()._set_control_value(value)
        event = wx.CommandEvent(wx.EVT_TOGGLEBUTTON.typeId, self.control.GetId())
        event.SetInt(value)
        wx.PostEvent(self.control.GetEventHandler(), event)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(
                wx.EVT_TOGGLEBUTTON,
                handler=self._update_value,
            )
        else:
            self.control.Bind(wx.EVT_TOGGLEBUTTON, self._update_value)
