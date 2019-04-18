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

""" The Qt-specific implementation of the spin field class """

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from traits.api import provides

from pyface.fields.i_spin_field import ISpinField, MSpinField
from pyface.qt.QtGui import QSpinBox
from .field import Field


@provides(ISpinField)
class SpinField(MSpinField, Field):
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

    def _get_control_value(self):
        return self.control.value()

    def _set_control_value(self, value):
        self.control.setValue(value)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.valueChanged[int].disconnect(self._value_updated)
        else:
            self.control.valueChanged[int].connect(self._value_updated)

    def _get_control_bounds(self):
        return (self.control.minimum(), self.control.maximum())

    def _set_control_bounds(self, bounds):
        self.control.setRange(*bounds)
