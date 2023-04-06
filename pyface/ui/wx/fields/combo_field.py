# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the combo field class """


import wx

from traits.api import provides

from pyface.fields.i_combo_field import IComboField, MComboField
from .editable_field import EditableField


@provides(IComboField)
class ComboField(MComboField, EditableField):
    """ The Wx-specific implementation of the combo field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = wx.Choice(parent, -1)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _update_value(self, event):
        """ Handle a change to the value from user interaction
        """
        # do normal focus event stuff
        if isinstance(event, wx.FocusEvent):
            event.Skip()
        if self.control is not None:
            self.value = self.values[event.GetInt()]

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        index = self.control.GetSelection()
        if index != -1:
            return self.values[index]
        else:
            raise IndexError("no value selected")

    def _get_control_text(self):
        """ Toolkit specific method to get the control's text content. """
        index = self.control.GetSelection()
        if index != -1:
            return self.control.GetString(index)
        else:
            raise IndexError("no value selected")

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        index = self.values.index(value)
        self.control.SetSelection(index)
        event = wx.CommandEvent(wx.EVT_CHOICE.typeId, self.control.GetId())
        event.SetInt(index)
        wx.PostEvent(self.control.GetEventHandler(), event)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(wx.EVT_CHOICE, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_CHOICE, self._update_value)

    def _get_control_text_values(self):
        """ Toolkit specific method to get the control's text values. """
        values = []
        for i in range(self.control.GetCount()):
            values.append(self.control.GetString(i))
        return values

    def _set_control_values(self, values):
        """ Toolkit specific method to set the control's values. """
        current_value = self.value
        self.control.Clear()
        for i, value in enumerate(values):
            item = self.formatter(value)
            if isinstance(item, tuple):
                image, text = item
            else:
                text = item
            self.control.Insert(text, i, value)

        if current_value in values:
            self._set_control_value(current_value)
        else:
            self._set_control_value(self.value)
