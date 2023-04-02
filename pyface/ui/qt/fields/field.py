# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Qt-specific implementation of the text field class """


from traits.api import Any, provides

from pyface.fields.i_field import IField, MField
from pyface.ui.qt.layout_widget import LayoutWidget
from pyface.ui.qt.util.alignment import (
    alignment_to_qalignment, qalignment_to_alignment
)


@provides(IField)
class Field(MField, LayoutWidget):
    """ The Qt-specific implementation of the field class

    This is an abstract class which is not meant to be instantiated.  Because
    many concrete QWidgets provide a `value` property, the default getters and
    setters target this.
    """

    #: The value held by the field.
    value = Any()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.value()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.setValue(value)

    def _get_control_alignment(self):
        """ Toolkit specific method to get the control's alignment. """
        # default implementation
        return qalignment_to_alignment(self.control.alignment())

    def _set_control_alignment(self, alignment):
        """ Toolkit specific method to set the control's alignment. """
        self.control.setAlignment(alignment_to_qalignment(alignment))
