# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Provides an N-dimensional array data model implementation.

This module provides a concrete implementation of a data model for an
n-dim numpy array.
"""
from traits.api import Array, Instance, observe

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.value_types.api import (
    ConstantValue, FloatValue, IntValue, TextValue, no_value
)
from pyface.data_view.index_manager import TupleIndexManager


class ArrayDataModel(AbstractDataModel):

    #: The array being displayed.  This must have dimension at least 2.
    data = Array()

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(TupleIndexManager, args=())

    #: The value type of the label headers.
    label_header_type = Instance(
        AbstractValueType,
        factory=ConstantValue,
        kw={'text': "Index"},
    )

    #: The value type of the column titles.
    column_header_type = Instance(
        AbstractValueType,
        factory=IntValue,
        kw={'is_editable': False},
    )

    #: The value type of the row titles.
    row_header_type = Instance(
        AbstractValueType,
        factory=IntValue,
        kw={'is_editable': False},
    )

    #: The type of value being displayed in the data model.
    value_type = Instance(AbstractValueType)

    # Data structure methods

    def get_column_count(self, row):
        """ How many columns in a row of the data view model.

        The total number of columns in the table is given by the column
        count of the Root row.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        column_count : non-negative int
            The number of columns that the row provides.
        """
        return self.data.shape[-1]

    def can_have_children(self, row):
        """ Whether or not a row can have child rows.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        can_have_children : bool
            Whether or not the row can ever have child rows.
        """
        if len(row) < self.data.ndim - 1:
            return True
        return False

    def get_row_count(self, row):
        """ Whether or not the row currently has any child rows.

        Subclasses may override this to provide a more direct implementation.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        has_children : bool
            Whether or not the row currently has child rows.
        """
        if len(row) < self.data.ndim - 1:
            return self.data.shape[len(row)]
        return 0

    # Data value methods

    def get_value(self, row, column):
        """ Return the Python value for the row and column.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        row_count : non-negative int
            The number of child rows that the row has.
        """
        if row == []:
            if column == []:
                return None
            return column[0]
        elif column == []:
            return row[-1]
        else:
            index = tuple(row + column)
            if len(index) != self.data.ndim:
                return None
            return self.data[index]

    def can_set_value(self, row, column):
        """ Whether the value in the indicated row and column can be set.

        This returns False for row and column headers, but True for all
        array values.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        can_set_value : bool
            Whether or not the value can be set.
        """
        # can only set values when we have the full index
        index = tuple(row + column)
        return len(index) == self.data.ndim

    def set_value(self, row, column, value):
        """ Return the Python value for the row and column.

        The values for column headers are returned by calling this method
        with row as Root.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 1.

        Returns
        -------
        value : any
            The value represented by the given row and column.
        """
        if self.can_set_value(row, column):
            index = tuple(row + column)
            self.data[index] = value
            self.values_changed = (row, column, row, column)
            return True

        return False

    def get_value_type(self, row, column):
        """ Return the text value for the row and column.

        The value type for column headers are returned by calling this method
        with row equal to [].  The value typess for row headers are returned
        by calling this method with column equal to [].

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        text : str
            The text to display in the given row and column.
        """
        if row == []:
            if column == []:
                return self.label_header_type
            return self.column_header_type
        elif column == []:
            return self.row_header_type
        elif len(row) < self.data.ndim - 1:
            return no_value
        else:
            return self.value_type

    # data update methods

    @observe('data', dispatch='ui')
    def data_updated(self, event):
        """ Handle the array being replaced with a new array. """
        if event.new.shape == event.old.shape:
            self.values_changed = (
                ([0], [0], [event.old.shape[0] - 1], [event.old.shape[-1] - 1])
            )
        else:
            self.structure_changed = True

    @observe('value_type.updated', dispatch='ui')
    def value_type_updated(self, event):
        """ Handle the value type being updated. """
        self.values_changed = (
            ([0], [0], [self.data.shape[0] - 1], [self.data.shape[-1] - 1])
        )

    @observe('column_header_type.updated', dispatch='ui')
    def column_header_type_updated(self, event):
        """ Handle the header type being updated. """
        self.values_changed = (
            ([], [0], [], [self.data.shape[-1] - 1])
        )

    @observe('row_header_type.updated', dispatch='ui')
    def value_header_type_updated(self, event):
        """ Handle the header type being updated. """
        self.values_changed = (
            ([0], [], [self.data.shape[0] - 1], [])
        )

    @observe('label_header_type.updated', dispatch='ui')
    def label_header_type_updated(self, event):
        """ Handle the header type being updated. """
        self.values_changed = (
            ([], [], [], [])
        )

    def _value_type_default(self):
        import numpy as np
        scalar_type = self.data.dtype
        if np.issubdtype(scalar_type, np.integer):
            return IntValue()
        elif np.issubdtype(scalar_type, np.floating):
            return FloatValue()
        elif np.issubdtype(scalar_type, np.character):
            return TextValue()

        return TextValue(is_editable=False)
