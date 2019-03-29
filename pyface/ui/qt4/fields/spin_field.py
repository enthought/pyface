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

from __future__ import absolute_import, print_function, unicode_literals

from traits.api import Bool, Enum, Str, Trait, provides

from pyface.fields.i_spin_field import ISpinField, MSpinField
from pyface.qt.QtGui import QSpinBox
from .field import Field


@provides(ISpinField)
class SpinField(MSpinField, Field):
    """ The Qt-specific implementation of the text field class """

    # ------------------------------------------------------------------------
    # IField interface
    # ------------------------------------------------------------------------

    def _initialize_control(self, control):
        super(SpinField, self)._initialize_control(control)
        control.setRange(self.minimum, self.maximum)
        control.setValue(self.value)

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = QSpinBox(parent)
        self._initialize_control(control)
        return control

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(SpinField, self)._add_event_listeners()
        if self.control is not None:
            self.control.valueChanged.connect(self._value_updated)

    def _remove_event_listeners(self, control):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            self.control.valueChanged.disconnect(self._value_updated)
        super(SpinField, self)._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _handle_update(self):
        if self.control is not None:
            value = self.control.value()
            self._value_updated(value)

    # Trait change handlers --------------------------------------------------

    def _value_changed(self, new):
        if self.control is not None and self.control.value() != new:
            self.control.setText(new)

    def _bounds_changed(self, new):
        if self.control is not None:
            self.control.setRange(*new)
