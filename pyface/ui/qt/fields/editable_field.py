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

from traits.api import provides

from pyface.fields.i_editable_field import IEditableField, MEditableField
from pyface.ui.qt.fields.field import Field


@provides(IEditableField)
class EditableField(MEditableField, Field):
    """ The Qt-specific implementation of the field class

    This is an abstract class which is not meant to be instantiated. Because
    many concrete QWidgets provide a `value` property, the default control
    observer targets this.
    """

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.valueChanged[int].disconnect(self._update_value)
        else:
            self.control.valueChanged[int].connect(self._update_value)
