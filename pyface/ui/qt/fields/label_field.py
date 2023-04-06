# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Qt-specific implementation of the label field class """


from traits.api import provides

from pyface.fields.i_label_field import ILabelField, MLabelField
from pyface.qt.QtGui import QLabel, QPixmap
from .field import Field


@provides(ILabelField)
class LabelField(MLabelField, Field):
    """ The Qt-specific implementation of the label field class """

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QLabel(parent)
        return control

    # Toolkit control interface ---------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.text()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        return self.control.setText(value)

    def _set_control_icon(self, icon):
        """ Toolkit specific method to set the control's icon. """
        if icon is not None:
            self.control.setPixmap(self.icon.create_bitmap())
        else:
            self.control.setPixmap(QPixmap())
