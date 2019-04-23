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

from __future__ import absolute_import, print_function, unicode_literals

from traits.api import Any, Instance, Unicode, provides

import wx

from pyface.fields.i_field import IField, MField
from pyface.ui.wx.widget import Widget


@provides(IField)
class Field(MField, Widget):
    """ The Wxspecific implementation of the field class

    This is an abstract class which is not meant to be instantiated.
    """

    #: The value held by the field.
    value = Any

    #: A tooltip for the field.
    tooltip = Unicode

    #: An optional context menu for the field.
    context_menu = Instance('pyface.action.menu_manager.MenuManager')

    # ------------------------------------------------------------------------
    # IField interface
    # ------------------------------------------------------------------------

    def _initialize_control(self):
        """ Perform any toolkit-specific initialization for the control. """
        self.control.SetToolTipString(self.tooltip)
        self.control.Enable(self.enabled)
        self.control.Show(self.visible)

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create(self):
        super(Field, self)._create()
        self._add_event_listeners()

    def destroy(self):
        self._remove_event_listeners()
        super(Field, self).destroy()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_tooltip(self):
        """ Toolkit specific method to get the control's tooltip. """
        return self.control.GetToolTipString()

    def _set_control_tooltip(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        self.control.SetToolTipString(tooltip)

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the control menu observer. """
        if remove:
            self.control.Unbind(wx.EVT_CONTEXT_MENU,
                                handler=self._handle_context_menu)
        else:
            self.control.Bind(wx.EVT_CONTEXT_MENU, self._handle_context_menu)

    def _handle_control_context_menu(self, event):
        """ Signal handler for displaying context menu. """
        if self.control is not None and self.context_menu is not None:
            menu = self.context_menu.create_menu(self.control)
            self.control.PopupMenu(menu)
