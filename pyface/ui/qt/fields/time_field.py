# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Qt-specific implementation of the time field class """


from traits.api import provides

from pyface.qt.QtGui import QTimeEdit

from pyface.fields.i_time_field import ITimeField, MTimeField
from pyface.ui.qt.util.datetime import pytime_to_qtime, qtime_to_pytime
from .editable_field import EditableField


@provides(ITimeField)
class TimeField(MTimeField, EditableField):
    """ The Qt-specific implementation of the time field class """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """

        control = QTimeEdit(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return qtime_to_pytime(self.control.time())

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.setTime(pytime_to_qtime(value))

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.timeChanged.disconnect(self._update_value)
        else:
            self.control.timeChanged.connect(self._update_value)
