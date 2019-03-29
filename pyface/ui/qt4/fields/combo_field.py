# Copyright (c) 2019, Enthought, Inc.
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

""" The Qt-specific implementation of the combo field class """

from __future__ import absolute_import, print_function, unicode_literals

from six import text_type

from traits.api import (
    Bool, Callable, Enum, List, Unicode, on_trait_change, provides
)

from pyface.fields.i_combo_field import IComboField, MComboField
from pyface.qt.QtGui import QComboBox
from .field import Field


@provides(IComboField)
class ComboField(MComboField, Field):
    """ The Qt-specific implementation of the text field class """

    # ------------------------------------------------------------------------
    # IField interface
    # ------------------------------------------------------------------------

    def _initialize_control(self, control):
        super(ComboField, self)._initialize_control(control)
        self._populate_values(control)
        control.setInsertPolicy(QComboBox.NoInsert)
        control.setEditable(self.editable)
        if self.editable:
            line_edit = control.lineEdit()
            line_edit.setText(self.edit_text)

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QComboBox(parent)
        self._initialize_control(control)
        return control

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        super(ComboField, self)._add_event_listeners()
        if self.control is not None:
            self.control.activated.connect(self._index_updated)
            if self.editable:
                line_edit = self.control.lineEdit()
                line_edit.editingFinished.connect(self._text_updated)

    def _remove_event_listeners(self, control):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None:
            self.control.activated.disconnect(self._index_updated)
            if self.editable:
                self.control.lineEdit().editingFinished.disconnect(
                    self._text_updated)
        super(ComboField, self)._remove_event_listeners()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _populate_values(self, control=None):
        if control is None:
            control = self.control
        if control is not None:
            control.clear()
            for value in self.values:
                value = self.formatter(value)
                if isinstance(value, tuple):
                    image, text = value
                    icon = image.create_icon()
                    control.addItem(icon, text)
                else:
                    control.addItem(value)
            self._update_value(control, self.value)

    def _update_value(self, control, value):
        if value in self.values:
            index = self.values.index(value)
        else:
            index = -1
        control.setCurrentIndex(index)

    def _index_updated(self, index):
        if index != -1:
            self._value_updated(self.values[index])
            value = self.formatter(self.value)
            if isinstance(value, tuple):
                self.edit_text = value[1]
            else:
                self.edit_text = value

    def _text_updated(self):
        if self.control and self.editable:
            line_edit = self.control.lineEdit()
            self.edit_text = line_edit.text()

    # Trait change handlers --------------------------------------------------

    def _edit_text_changed(self, text):
        if self.control is not None and self.editable:
            line_edit = self.control.lineEdit()
            line_edit.setText(text)
