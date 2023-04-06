# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Qt-specific implementation of the toggle field class """


from traits.api import provides

from pyface.fields.i_toggle_field import IToggleField, MToggleField
from pyface.qt.QtGui import (
    QCheckBox, QIcon, QPushButton, QRadioButton
)
from .editable_field import EditableField


@provides(IToggleField)
class ToggleField(MToggleField, EditableField):
    """ The Qt-specific implementation of the toggle field class """

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.isChecked()

    def _get_control_text(self):
        """ Toolkit specific method to get the control's text. """
        return self.control.text()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        return self.control.setChecked(value)

    def _set_control_text(self, text):
        """ Toolkit specific method to set the control's text. """
        return self.control.setText(text)

    def _set_control_icon(self, icon):
        """ Toolkit specific method to set the control's icon. """
        if icon is not None:
            self.control.setIcon(icon.create_icon())
        else:
            self.control.setIcon(QIcon())

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.toggled.disconnect(self._update_value)
        else:
            self.control.toggled.connect(self._update_value)

    def _get_control_alignment(self):
        """ Toolkit specific method to get the control's alignment. """
        # dummy implementation
        return self.alignment

    def _set_control_alignment(self, alignment):
        """ Toolkit specific method to set the control's alignment. """
        # use stylesheet for button alignment
        self.control.setStyleSheet(f"text-align: {alignment}")


class CheckBoxField(ToggleField):
    """ The Qt-specific implementation of the checkbox class """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QCheckBox(parent)
        return control


class RadioButtonField(ToggleField):
    """ The Qt-specific implementation of the radio button class

    This is intended to be used in groups, and shouldn't be used by itself.
    """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QRadioButton(parent)
        return control


class ToggleButtonField(ToggleField):
    """ The Qt-specific implementation of the toggle button class """

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QPushButton(parent)
        control.setCheckable(True)
        return control
