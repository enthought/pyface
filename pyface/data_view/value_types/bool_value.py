# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Str

from pyface.data_view.abstract_value_type import AbstractValueType, CheckState


class BoolValue(AbstractValueType):
    """ Value that presents a boolean value via checked state.
    """

    #: The text to display next to a True value.
    true_text = Str()

    #: The text to display next to a False value.
    false_text = Str()

    def has_editor_value(self, model, row, column):
        """ BoolValues don't use editors, but have always-on checkbox.

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
        has_editor_value : bool
            Whether or not the value is editable.
        """
        return False

    def get_text(self, model, row, column):
        """ The textual representation of the underlying value.


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
            The textual representation of the underlying value.
        """
        return (
            self.true_text if model.get_value(row, column) else self.false_text
        )

    def has_check_state(self, model, row, column):
        """ Whether or not the value has checked state.

        The default implementation returns True.

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
        has_check_state : bool
            Whether or not the value has a checked state.
        """
        return True

    def set_check_state(self, model, row, column, check_state):
        """ Set the boolean value from the check state.

        Parameters
        ----------
        model : AbstractDataModel
            The data model holding the data.
        row : sequence of int
            The row in the data model being set.
        column : sequence of int
            The column in the data model being set.
        check_state : "checked" or "unchecked"
            The check state being set.

        Raises
        -------
        DataViewSetError
            If the value cannot be set.
        """
        value = (check_state == CheckState.CHECKED)
        model.set_value(row, column, value)
