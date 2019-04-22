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
""" The Qt-specific implementation of the text field class """

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from traits.api import Any, Instance, Unicode, provides

from pyface.qt.QtCore import Qt
from pyface.fields.i_field import IField, MField
from pyface.ui.qt4.widget import Widget


@provides(IField)
class Field(MField, Widget):
    """ The Qt-specific implementation of the field class

    This is an abstract class which is not meant to be instantiated.
    """

    #: The value held by the field.
    value = Any

    #: A tooltip for the field.
    tooltip = Unicode

    #: An optional context menu for the field.
    context_menu = Instance('pyface.action.menu_manager.MenuManager')

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_tooltip(self):
        """ Toolkit specific method to get the control's tooltip. """
        return self.control.toolTip()

    def _set_control_tooltip(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        self.control.setToolTip(tooltip)

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the control menu observer. """
        if remove:
            self.control.setContextMenuPolicy(Qt.DefaultContextMenu)
            self.control.customContextMenuRequested.disconnect(
                self._handle_control_context_menu)
        else:
            self.control.customContextMenuRequested.connect(
                self._handle_control_context_menu)
            self.control.setContextMenuPolicy(Qt.CustomContextMenu)

    def _handle_control_context_menu(self, pos):
        """ Signal handler for displaying context menu. """
        if self.control is not None and self.context_menu is not None:
            menu = self.context_menu.create_menu(self.control)
            menu.show(pos.x(), pos.y())
