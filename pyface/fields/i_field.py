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

from traits.api import Any, Bool, HasTraits, Instance, Unicode

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

    def _initialize_control(self, control):
        """ Perform any toolkit-specific initialization for the control. """


class MField(HasTraits):
    """ The field mix-in. """

    def _value_updated(self, value):
        """ Handle a change to the value from user interaction

        This is a method suitable for calling from a toolkit event handler.
        """
        self.value = value
