# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the time field class """

from datetime import time

import wx.adv

from traits.api import provides

from pyface.fields.i_time_field import ITimeField, MTimeField
from .editable_field import EditableField


@provides(ITimeField)
class TimeField(MTimeField, EditableField):
    """ The Wx-specific implementation of the time field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = wx.adv.TimePickerCtrl(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return time(*self.control.GetTime())

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.SetTime(value.hour, value.minute, value.second)
        wxdatetime = wx.DateTime.Now()
        wxdatetime.SetHour(value.hour)
        wxdatetime.SetMinute(value.minute)
        wxdatetime.SetSecond(value.second)
        event = wx.adv.DateEvent(
            self.control,
            wxdatetime,
            wx.adv.EVT_TIME_CHANGED.typeId
        )
        wx.PostEvent(self.control.GetEventHandler(), event)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(
                wx.adv.EVT_TIME_CHANGED,
                handler=self._update_value
            )
        else:
            self.control.Bind(wx.adv.EVT_TIME_CHANGED, self._update_value)
