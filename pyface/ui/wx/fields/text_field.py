#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
""" The Wx-specific implementation of the text field class """

from __future__ import print_function, absolute_import

from contextlib import contextmanager

import wx

from traits.api import Int, provides

from pyface.fields.i_text_field import ITextField, MTextField
from .field import Field


@provides(ITextField)
class TextField(MTextField, Field):
    """ The Wx-specific implementation of the text field class """

    #: Zero if not updating, positive if updating.
    _updating = Int

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        style = wx.TE_PROCESS_ENTER
        if self.echo == 'password':
            style |= wx.TE_PASSWORD

        control = wx.TextCtrl(parent, -1, value=self.value, style=style)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _update_value(self, event):
        # do normal focus event stuff
        if isinstance(event, wx.FocusEvent):
            event.Skip()
        if self.control is not None and self._updating == 0:
            self.value = self.control.GetValue()

    @contextmanager
    def _no_update(self):
        self._updating += 1
        try:
            yield
        finally:
            self._updating -= 1

    def _get_control_value(self):
        return self.control.GetValue()

    def _set_control_value(self, value):
        self.control.SetValue(value)

    def _observe_control_value(self, remove=False):
        if remove:
            self.control.Unbind(wx.EVT_TEXT, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_TEXT, self._update_value)

    def _get_control_placeholder(self):
        """ Toolkit specific method to set the control's placeholder. """
        return self.control.GetHint()

    def _set_control_placholder(self, placeholder):
        """ Toolkit specific method to set the control's placeholder. """
        self.control.SetHint(placeholder)

    def _get_control_echo(self):
        return self.echo

    def _set_control_echo(self, echo):
        # Can't change echo on Wx after control has been created."
        pass

    def _get_control_read_only(self):
        """ Toolkit specific method to get the control's read_only state. """
        return self.control.GetEditable()

    def _set_control_read_only(self, read_only):
        """ Toolkit specific method to set the control's read_only state. """
        self.control.SetEditable(not read_only)

    def _observe_control_editing_finished(self, remove=False):
        """ Change observation of whether editing is finished. """
        if remove:
            self.control.Unbind(wx.EVT_TEXT_ENTER, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_TEXT_ENTER, self._update_value)
