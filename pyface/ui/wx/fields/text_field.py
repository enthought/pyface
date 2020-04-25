# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the text field class """


import wx

from traits.api import provides

from pyface.fields.i_text_field import ITextField, MTextField
from .field import Field


ALIGNMENT_TO_WX_ALIGNMENT = {
    'default': wx.TE_LEFT,
    'left': wx.TE_LEFT,
    'center': wx.TE_CENTRE,
    'right': wx.TE_RIGHT,
}
WX_ALIGNMENT_TO_ALIGNMENT = {
    0: 'default',
    wx.TE_LEFT: 'left',
    wx.TE_CENTRE: 'center',
    wx.TE_RIGHT: 'right',
}

ALIGNMENT_MASK = wx.TE_LEFT | wx.TE_CENTRE | wx.TE_RIGHT


@provides(ITextField)
class TextField(MTextField, Field):
    """ The Wx-specific implementation of the text field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        style = wx.TE_PROCESS_ENTER
        if self.echo == "password":
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
        if self.control is not None:
            self.value = self.control.GetValue()

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.GetValue()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.SetValue(value)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.Unbind(wx.EVT_TEXT, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_TEXT, self._update_value)

    def _get_control_placeholder(self):
        """ Toolkit specific method to set the control's placeholder. """
        return self.control.GetHint()

    def _set_control_placeholder(self, placeholder):
        """ Toolkit specific method to set the control's placeholder. """
        self.control.SetHint(placeholder)

    def _get_control_echo(self):
        """ Toolkit specific method to get the control's echo. """
        return self.echo

    def _set_control_echo(self, echo):
        """ Toolkit specific method to set the control's echo. """
        # Can't change echo on Wx after control has been created."
        pass

    def _get_control_read_only(self):
        """ Toolkit specific method to get the control's read_only state. """
        return not self.control.IsEditable()

    def _set_control_read_only(self, read_only):
        """ Toolkit specific method to set the control's read_only state. """
        self.control.SetEditable(not read_only)

    def _get_control_alignment(self):
        """ Toolkit specific method to get the control's read_only state. """
        alignment = self.control.GetWindowStyle() & ALIGNMENT_MASK
        return WX_ALIGNMENT_TO_ALIGNMENT[alignment]

    def _set_control_alignment(self, alignment):
        """ Toolkit specific method to set the control's read_only state. """
        other_styles = self.control.GetWindowStyle() & ~ALIGNMENT_MASK
        window_style = other_styles | ALIGNMENT_TO_WX_ALIGNMENT[alignment]
        self.control.SetWindowStyle(window_style)
        self.control.Refresh()

    def _observe_control_editing_finished(self, remove=False):
        """ Change observation of whether editing is finished. """
        if remove:
            self.control.Unbind(wx.EVT_TEXT_ENTER, handler=self._update_value)
        else:
            self.control.Bind(wx.EVT_TEXT_ENTER, self._update_value)
