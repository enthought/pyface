# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the text field class """


from traits.api import provides

from pyface.fields.i_field import IField, MField
from pyface.ui.wx.layout_widget import LayoutWidget
from pyface.ui.wx.util.alignment import (
    get_alignment_style, set_alignment_style
)


@provides(IField)
class Field(MField, LayoutWidget):
    """ The Wx-specific implementation of the field class

    This is an abstract class which is not meant to be instantiated.
    """

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_alignment(self):
        """ Toolkit specific method to get the control's read_only state. """
        return get_alignment_style(self.control.GetWindowStyle())

    def _set_control_alignment(self, alignment):
        """ Toolkit specific method to set the control's read_only state. """
        old_style = self.control.GetWindowStyle()
        new_style = set_alignment_style(alignment, old_style)
        self.control.SetWindowStyle(new_style)
        self.control.Refresh()
