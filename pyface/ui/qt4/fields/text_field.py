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

from traits.api import Trait, provides

from pyface.fields.i_text_field import ITextField, MTextField
from pyface.qt.QtGui import QLineEdit
from .field import Field


# mapped trait for Qt line edit echo modes
Echo = Trait(
    'normal',
    {
        'normal': QLineEdit.EchoMode.Normal,
        'password': QLineEdit.EchoMode.Password,
        'none': QLineEdit.EchoMode.NoEcho,
        'when_editing': QLineEdit.EchoMode.PasswordEchoOnEdit,
    }
)


@provides(ITextField)
class TextField(MTextField, Field):
    """ The Qt-specific implementation of the text field class """

    #: Display typed text, or one of several hidden "password" modes.
    echo = Echo

    # ------------------------------------------------------------------------
    # IField interface
    # ------------------------------------------------------------------------

    def _initialize_control(self, control):
        super(TextField, self)._initialize_control(control)
        control.setEchoMode(self.echo_)
        control.setText(self.value)
        control.setPlaceholderText(self.placeholder)
        control.setReadOnly(self.read_only)

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QLineEdit(parent)
        self._initialize_control(control)
        return control

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(TextField, self)._add_event_listeners()
        if self.control is not None:
            if self.update_text == 'editing_finished':
                self.control.editingFinished.connect(self._handle_update)
            else:
                self.control.textEdited.connect(self._handle_update)

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            if self.update_text == 'editing_finished':
                self.control.editingFinished.disconnect(self._handle_update)
            else:
                self.control.textEdited.disconnect(self._handle_update)
        super(TextField, self)._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _handle_update(self):
        if self.control is not None:
            value = self.control.text()
            self._value_updated(value)

    # Trait change handlers --------------------------------------------------

    def _value_changed(self, new):
        if self.control is not None and self.control.text() != new:
            self.control.setText(new)

    def _update_text_changed(self, new):
        if self.control is not None:
            if new == 'editing_finished':
                self.control.editingFinished.disconnect(self._handle_update)
                self.control.textEdited.connect(self._handle_update)
            else:
                self.control.textEdited.disconnect(self._handle_update)
                self.control.editingFinished.connect(self._handle_update)

    def _placeholder_changed(self, new):
        if self.control is not None:
            self.control.setPlaceholderText(new)

    def _echo_changed(self):
        if self.control is not None:
            self.control.setEchoMode(self.echo_)

    def _read_only_changed(self, new):
        if self.control is not None:
            self.control.setReadOnly(new)
