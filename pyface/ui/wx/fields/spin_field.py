# Copyright (c) 2017-19, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>

""" The Wx-specific implementation of the spin field class """

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import wx

from traits.api import provides

from pyface.fields.i_spin_field import ISpinField, MSpinField
from .field import Field


@provides(ISpinField)
class SpinField(MSpinField, Field):
    """ The Wx-specific implementation of the spin field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = wx.SpinCtrl(parent, style=wx.TE_PROCESS_ENTER)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.GetValue()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.SetValue(value)
        event = wx.SpinEvent(wx.EVT_SPINCTRL.typeId, self.control.GetId())
        event.SetInt(value)
        wx.PostEvent(self.control.GetEventHandler(), event)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(wx.EVT_SPINCTRL, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_SPINCTRL, self._update_value)

    def _get_control_bounds(self):
        """ Toolkit specific method to get the control's bounds. """
        return (self.control.GetMin(), self.control.GetMax())

    def _set_control_bounds(self, bounds):
        """ Toolkit specific method to set the control's bounds. """
        self.control.SetRange(*bounds)
