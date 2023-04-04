# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import locale
from math import inf

from traits.api import Callable, Float

from pyface.data_view.data_view_errors import DataViewSetError
from .editable_value import EditableValue


def format_locale(value):
    return "{:n}".format(value)


class NumericValue(EditableValue):
    """ Data channels for a numeric value.
    """

    #: The minimum value for the numeric value.
    minimum = Float(-inf)

    #: The maximum value for the numeric value.
    maximum = Float(inf)

    #: A function that converts to the numeric type.
    evaluate = Callable()

    #: A function that converts the required type to a string for display.
    format = Callable(format_locale, update_value_type=True)

    #: A function that converts the required type from a display string.
    unformat = Callable(locale.delocalize)

    def is_valid(self, model, row, column, value):
        """ Whether or not the value within the specified range.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being queried.
        column : sequence of int
            The column in the data model being queried.
        value : Any
            The value to validate.

        Returns
        -------
        is_valid : bool
            Whether or not the value is valid.
        """
        try:
            return self.minimum <= value <= self.maximum
        except Exception:
            return False

    def get_editor_value(self, model, row, column):
        """ Get the numerical value for the editor to use.

        This uses the evaluate method to convert the underlying value to a
        number.

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
        editor_value : number
            Whether or not the value is editable.
        """
        # evaluate is needed to convert numpy types to python types so
        # Qt recognises them
        return self.evaluate(model.get_value(row, column))

    def get_text(self, model, row, column):
        """ Get the display text from the underlying value.

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
            The text to display.
        """
        return self.format(model.get_value(row, column))

    def set_text(self, model, row, column, text):
        """ Set the text of the underlying value.

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

        Raises
        -------
        DataViewSetError
            If the value cannot be set.
        """
        try:
            value = self.evaluate(self.unformat(text))
        except ValueError:
            raise DataViewSetError(
                "Can't evaluate value: {!r}".format(text)
            )
        self.set_editor_value(model, row, column, value)


class IntValue(NumericValue):
    """ Data channels for an integer value.
    """

    evaluate = Callable(int)


class FloatValue(NumericValue):
    """ Data channels for a floating point value.
    """

    evaluate = Callable(float)
