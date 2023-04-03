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

""" The Qt-specific implementation of the combo field class """


from traits.api import provides

from pyface.fields.i_combo_field import IComboField, MComboField
from pyface.qt.QtCore import Qt
from pyface.qt.QtGui import QComboBox
from pyface.ui.qt.util.alignment import (
    alignment_to_qalignment, qalignment_to_alignment
)
from .editable_field import EditableField


@provides(IComboField)
class ComboField(MComboField, EditableField):
    """ The Qt-specific implementation of the combo field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QComboBox(parent)
        control.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        control.setEditable(False)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        index = self.control.currentIndex()
        if index != -1:
            return self.control.itemData(index)
        else:
            raise IndexError("no value selected")

    def _get_control_text(self):
        """ Toolkit specific method to get the control's value. """
        index = self.control.currentIndex()
        if index != -1:
            return self.control.itemData(index, Qt.ItemDataRole.DisplayRole)
        else:
            raise IndexError("no value selected")

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        index = self.values.index(value)
        self.control.setCurrentIndex(index)
        self.control.activated.emit(index)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.activated.disconnect(self._update_value)
        else:
            self.control.activated.connect(self._update_value)

    def _get_control_text_values(self):
        """ Toolkit specific method to get the control's values. """
        model = self.control.model()
        values = []
        for i in range(model.rowCount()):
            values.append(model.item(i))
        return values

    def _set_control_values(self, values):
        """ Toolkit specific method to set the control's values. """
        current_value = self.value
        self.control.clear()
        for value in self.values:
            item = self.formatter(value)
            if isinstance(item, tuple):
                image, text = item
                icon = image.create_icon()
                self.control.addItem(icon, text, userData=value)
            else:
                self.control.addItem(item, userData=value)
        if current_value in values:
            self._set_control_value(current_value)
        else:
            self._set_control_value(self.value)

    def _get_control_alignment(self):
        """ Toolkit specific method to get the control's alignment. """
        # only works if combobox is ieditable, which currently is always False
        line_edit = self.control.lineEdit()
        if line_edit is not None:
            return qalignment_to_alignment(line_edit.alignment())
        else:
            # no widget; cheat
            return self.alignment

    def _set_control_alignment(self, alignment):
        """ Toolkit specific method to set the control's alignment. """
        line_edit = self.control.lineEdit()
        if line_edit is not None:
            return line_edit.setAlignment(alignment_to_qalignment(alignment))
