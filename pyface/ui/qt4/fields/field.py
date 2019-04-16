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
    # IField interface
    # ------------------------------------------------------------------------

    def _initialize_control(self, control):
        """ Perform any toolkit-specific initialization for the control. """
        control.setToolTip(self.tooltip)
        control.setEnabled(self.enabled)
        control.setVisible(self.visible)

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(Field, self)._add_event_listeners()
        if self.control is not None:
            self.control.customContextMenuRequested.connect(
                    self._handle_context_menu)
            self.control.contextMenuPolicy(Qt.CustomContextMenu)

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            self.control.customContextMenuRequested.disconnect(
                    self._handle_context_menu)
        super(Field, self)._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _handle_context_menu(self, pos):
        """ Signal handler for displaying context menu. """
        if self.control is not None and self.context_menu is not None:
            menu = self.context_menu.create_menu(self.control)
            menu.show(pos.x(), pos.y())

    # Trait change handlers --------------------------------------------------

    def _tooltip_changed(self, new):
        if self.control is not None:
            self.control.setToolTip(new)

    def _context_menu_changed(self, old, new):
        if self.control is not None:
            if new is None:
                #: we no longer have a context menu
                self.control.contextMenuPolicy(Qt.DefaultContextMenu)
            else:
                self.control.contextMenuPolicy(Qt.CustomContextMenu)
