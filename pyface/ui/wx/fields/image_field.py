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

from pyface.ui.wx.fields.field import Field
from pyface.fields.i_image_field import IImageField, MImageField
from pyface.wx.image_control import ImageControl


@provides(IImageField)
class ImageField(MImageField, Field):
    """ The Wx-specific implementation of the image field class

    """

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = ImageControl(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        # XXX we should really have a ToolkitImage subclass of Image and
        # which would be the correct subclass to return.
        return self.control.GetBitmap()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        if value is None:
            self._toolkit_value = None
        else:
            self._toolkit_value = self.value.create_bitmap()
        self.control.SetBitmap(self._toolkit_value)
