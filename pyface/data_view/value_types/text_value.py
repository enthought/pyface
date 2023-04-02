# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Callable

from .editable_value import EditableValue


class TextValue(EditableValue):
    """ Editable value that presents a string value.
    """

    #: A function that converts the value to a string for display.
    format = Callable(str, update_value_type=True)

    #: A function that converts to a value from a display string.
    unformat = Callable(str)

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
        value = self.unformat(text)
        self.set_editor_value(model, row, column, value)
