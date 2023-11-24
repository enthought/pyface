# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>

""" The Qt-specific implementation of the spin field class """


from traits.api import provides

from pyface.fields.i_spin_field import ISpinField, MSpinField
from pyface.qt.QtGui import QSpinBox
from .editable_field import EditableField


@provides(ISpinField)
class SpinField(MSpinField, EditableField):
    """ The Qt-specific implementation of the spin field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = QSpinBox(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_bounds(self):
        """ Toolkit specific method to get the control's bounds. """
        return (self.control.minimum(), self.control.maximum())

    def _set_control_bounds(self, bounds):
        """ Toolkit specific method to set the control's bounds. """
        self.control.setRange(*bounds)

    def _get_control_wrap(self):
        """ Toolkit specific method to get whether the control wraps. """
        return self.control.wrapping()

    def _set_control_wrap(self, wrap):
        """ Toolkit specific method to set whether the control wraps. """
        self.control.setWrapping(wrap)
