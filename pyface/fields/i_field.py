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
""" The text field interface. """

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from traits.api import Any, HasTraits, Instance, Unicode

from pyface.i_widget import IWidget


class IField(IWidget):
    """ The field interface.

    A field is a widget that displays a value and (potentially) allows a user
    to interact with it.
    """

    #: The value held by the field.
    value = Any

    #: A tooltip for the field.
    tooltip = Unicode

    #: An optional context menu for the field.
    context_menu = Instance('pyface.action.menu_manager.MenuManager')

    def show_context_menu(self, x, y):
        """ Create and show the context menu at a position. """

    def _initialize_control(self, control):
        """ Perform any toolkit-specific initialization for the control. """


class MField(HasTraits):
    """ The field mix-in. """

    #: The value held by the field.
    value = Any

    #: A tooltip for the field.
    tooltip = Unicode

    #: An optional context menu for the field.
    context_menu = Instance('pyface.action.menu_manager.MenuManager')

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(MField, self)._add_event_listeners()
        self.on_trait_change(self._value_updated, 'value', dispatch='ui')
        self.on_trait_change(self._tooltip_updated, 'tooltip', dispatch='ui')
        self.on_trait_change(self._context_menu_updated, 'context_menu',
                             dispatch='ui')
        if self.control is not None and self.context_menu is not None:
            self._observe_control_context_menu()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None and self.context_menu is not None:
            self._observe_control_context_menu(remove=True)
        self.on_trait_change(self._value_updated, 'value', dispatch='ui',
                             remove=True)
        self.on_trait_change(self._tooltip_updated, 'tooltip', dispatch='ui',
                             remove=True)
        self.on_trait_change(self._context_menu_updated, 'context_menu',
                             dispatch='ui', remove=True)
        super(MField, self)._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _create(self):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        self.control = self._create_control(self.parent)
        self._initialize_control()
        self._add_event_listeners()

        self.show(self.visible)
        self.enable(self.enabled)

    def _initialize_control(self):
        """ Perform any toolkit-specific initialization for the control. """
        self._set_control_tooltip(self.tooltip)

    def _update_value(self, value):
        """ Handle a change to the value from user interaction

        This is a method suitable for calling from a toolkit event handler.
        """
        self.value = self._get_control_value()

    def _get_control(self):
        """ If control is not passed directly, get it from the trait. """
        control = self.control
        if control is None:
            raise RuntimeError("Toolkit control does not exist.")
        return control

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        raise NotImplementedError

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        raise NotImplementedError

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        raise NotImplementedError

    def _get_control_tooltip(self):
        """ Toolkit specific method to get the control's tooltip. """
        raise NotImplementedError

    def _set_control_tooltip(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        raise NotImplementedError

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the control menu observer.

        This should use _handle_control_context_menu as the event handler.
        """
        raise NotImplementedError

    def _handle_control_context_menu(self, event):
        """ Handle a context menu event.

        This should call show_context_menu with appropriate position x and y
        arguments.

        The function signature will likely vary from toolkit to toolkit.
        """
        raise NotImplementedError

    # Trait change handlers -------------------------------------------------

    def _value_updated(self, value):
        if self.control is not None:
            self._set_control_value(value)

    def _tooltip_updated(self, tooltip):
        if self.control is not None:
            self._set_control_tooltip(tooltip)

    def _context_menu_updated(self, old, new):
        if self.control is not None:
            if new is None:
                self._observe_control_context_menu(remove=True)
            if old is None:
                self._observe_control_context_menu()
