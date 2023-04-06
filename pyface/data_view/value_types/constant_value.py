# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Str, Union, observe

from pyface.ui_traits import PyfaceColor
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.ui_traits import Image


class ConstantValue(AbstractValueType):
    """ A value type that does not depend on the underlying data model.

    This value type is not editable, but the other data channels it
    provides can be modified by changing the appropriate trait on the
    value type.
    """

    #: The text value to display.
    text = Str(update_value_type=True)

    #: The color value to display or None if no color.
    color = Union(None, PyfaceColor)

    #: The image value to display.
    image = Image(update_value_type=True)

    #: The tooltip value to display.
    tooltip = Str(update_value_type=True)

    def has_editor_value(self, model, row, column):
        return False

    def get_text(self, model, row, column):
        return self.text

    def has_color(self, model, row, column):
        """ Whether or not the value has color data.

        Returns true if the supplied color is not None.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        has_color : bool
            Whether or not the value has data-associated color
            values.
        """
        return self.color is not None

    def get_color(self, model, row, column):
        """ Get data-associated colour values for the given item.

        The default implementation returns white.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.

        Returns
        -------
        color : Color
            The color associated with the cell.
        """
        return self.color

    def has_image(self, model, row, column):
        return self.image is not None

    def get_image(self, model, row, column):
        if self.image is not None:
            return self.image
        return super().get_image(model, row, column)

    def get_tooltip(self, model, row, column):
        return self.tooltip

    @observe('color.rgba')
    def _color_updated(self, event):
        self.updated = True
