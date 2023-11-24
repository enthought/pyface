# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the label field class """

import wx

from traits.api import provides

from pyface.fields.i_label_field import ILabelField, MLabelField
from .field import Field


@provides(ILabelField)
class LabelField(MLabelField, Field):
    """ The Wx-specific implementation of the label field class """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = wx.StaticText(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.GetLabel()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.SetLabel(value)

    def _set_control_icon(self, icon):
        """ Toolkit specific method to set the control's icon. """
        # don't support icons on Wx for now
        pass
