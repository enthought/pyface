# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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
from traits.api import Array, HasRequiredTraits, Instance, observe

from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.data_view_errors import DataViewSetError
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.value_types.api import (
    ConstantValue, IntValue, no_value
)
from pyface.data_view.index_manager import TupleIndexManager


class _AtLeastTwoDArray(Array):
    """ Trait type that holds an array that at least two dimensional.
    """

    def validate(self, object, name, value):
        value = super().validate(object, name, value)
        if value.ndim == 0:
            value = value.reshape((0, 0))
        elif value.ndim == 1:
            value = value.reshape((-1, 1))
        return value


class ArrayDataModel(AbstractDataModel, HasRequiredTraits):
    """ A data model for an n-dim array.

    This data model presents the data from a multidimensional array
    hierarchically by dimension.  The underlying array must be at least 2
    dimensional.

    Values are adapted by the ``value_type`` trait.  This provides sensible
    default values for integer, float and text dtypes, but other dtypes may
    need the user of the class to supply an appropriate value type class to
    adapt values.

    There are additional value types which provide data sources for row
    headers, column headers, and the label of the row header column.  The
    defaults are likely suitable for most cases, but can be overriden if
    required.
    """

    #: The array being displayed.  This must have dimension at least 2.
    data = _AtLeastTwoDArray()

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(TupleIndexManager, args=())

    #: The value type of the row index column header.
    label_header_type = Instance(
        AbstractValueType,
        factory=ConstantValue,
        kw={'text': "Index"},
        allow_none=False,
    )

    #: The value type of the column titles.
    column_header_type = Instance(
        AbstractValueType,
        factory=IntValue,
        kw={'is_editable': False},
        allow_none=False,
    )

    #: The value type of the row titles.
    row_header_type = Instance(
        AbstractValueType,
        factory=IntValue,
        kw={'is_editable': False},
        allow_none=False,
    )

    #: The type of value being displayed in the data model.
    value_type = Instance(AbstractValueType, allow_none=False, required=True)

    # Data structure methods

    def get_column_count(self):
        """ How many columns in the data view model.

        The number of columns is the size of the last dimension of the array.

        Returns
        -------
        column_count : non-negative int
            The number of columns in the data view model, which is the size of
            the last dimension of the array.
        """
        return self.data.shape[-1]

    def can_have_children(self, row):
        """ Whether or not a row can have child rows.

        A row is a leaf row if the length of the index is one less than
        the dimension of the array: the final coordinate for the value will
        be supplied by the column index.

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

        The number of rows in a non-leaf row is equal to the size of the
        next dimension.

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
        if len(row) == 0:
            if len(column) == 0:
                return None
            return column[0]
        elif len(column) == 0:
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

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 1.

        Returns
        -------
        value : Any
            The value represented by the given row and column.
        """
        if self.can_set_value(row, column):
            index = tuple(row + column)
            self.data[index] = value
            self.values_changed = (row, column, row, column)
        else:
            raise DataViewSetError()

    def get_value_type(self, row, column):
        """ Return the value type of the given row and column.

        This method returns the value of ``column_header_type`` for column
        headers, the value of ``row_header_type`` for row headers, the value
        of ``label_header_type`` for the top-left corner value, the value of
        ``value_type`` for all array values, and ``no_value`` for everything
        else.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        value_type : AbstractValueType
            The value type of the given row and column.
        """
        if len(row) == 0:
            if len(column) == 0:
                return self.label_header_type
            return self.column_header_type
        elif len(column) == 0:
            return self.row_header_type
        elif len(row) < self.data.ndim - 1:
            return no_value
        else:
            return self.value_type

    # data update methods

    @observe('data')
    def data_updated(self, event):
        """ Handle the array being replaced with a new array. """
        if event.new.shape == event.old.shape:
            if self.data.size > 0:
                self.values_changed = (
                    (0,), (0,),
                    (event.old.shape[0] - 1,), (event.old.shape[-1] - 1,)
                )
        else:
            self.structure_changed = True

    @observe('value_type.updated')
    def value_type_updated(self, event):
        """ Handle the value type being updated. """
        if self.data.size > 0:
            self.values_changed = (
                (0,), (0,), (self.data.shape[0] - 1,), (self.data.shape[-1] - 1,)
            )

    @observe('column_header_type.updated')
    def column_header_type_updated(self, event):
        """ Handle the column header type being updated. """
        if self.data.shape[-1] > 0:
            self.values_changed = ((), (0,), (), (self.data.shape[-1] - 1,))

    @observe('row_header_type.updated')
    def value_header_type_updated(self, event):
        """ Handle the value header type being updated. """
        if self.data.shape[0] > 0:
            self.values_changed = ((0,), (), (self.data.shape[0] - 1,), ())

    @observe('label_header_type.updated')
    def label_header_type_updated(self, event):
        """ Handle the label header type being updated. """
        self.values_changed = ((), (), (), ())

    # default array value

    def _data_default(self):
        from numpy import zeros
        return zeros(shape=(0, 0))
