# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from .editable_value import EditableValue


class TextValue(EditableValue):
    """ Editable value that presents a string value.
    """

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

        Returns
        -------
        success : bool
            Whether or not the value was successfully set.
        """
        if model.can_set_value(row, column):
            return model.set_value(row, column, text)

        return False
