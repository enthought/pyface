# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.color import Color

from pyface.data_view.abstract_data_model import DataViewSetError
from .editable_value import EditableValue


class ColorValue(EditableValue):
    """ Editable value that presents a color value.

    This is suitable for use where the value returned by an item in
    the model is a Color object.
    """

    def is_valid(self, model, row, column, value):
        """ Is the given value valid for this item.

        The default implementation says the value must be a Color.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        value : Any
            The value to test.

        Returns
        -------
        success : bool
            Whether or not the value is valid.
        """
        return isinstance(value, Color)

    def get_editor_value(self, model, row, column):
        """ Get the editable representation of the underlying value.

        The default uses a text hex representation of the color.

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
        text : str
            A hex string representation of the colour.
        """
        return model.get_value(row, column).hex()

    def set_editor_value(self, model, row, column, value):
        """ Set the editable representation of the underlying value.

        The default expects a string that can be parsed to a color value.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        value : str
            A string that can be parsed to a color value.

        Returns
        -------
        success : bool
            Whether or not the value was successfully set.
        """
        try:
            color = Color.from_str(value)
        except Exception:
            raise DataViewSetError()
        return super().set_editor_value(model, row, column, color)

    def get_text(self, model, row, column):
        """ Get the textual representation of the underlying value.

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
        text : str
            A hex string representation of the colour.
        """
        return model.get_value(row, column).hex()

    def set_text(self, model, row, column, text):
        """ Set the textual representation of the underlying value.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        text : str
            The text to set.

        Returns
        -------
        success : bool
            Whether or not the value was successfully set.
        """
        return self.set_editor_value(model, row, column, text)

    def has_color(self, model, row, column):
        """ Whether or not the value has color data.

        The default implementation returns False.

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
        return True

    def get_color(self, model, row, column):
        """ Get data-associated colour values for the given item.

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
        return model.get_value(row, column)
