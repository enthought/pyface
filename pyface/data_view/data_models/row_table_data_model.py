# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A row-oriented data model implementation.

This module provides a concrete implementation of a data model for the
case of non-hierarchical, row-oriented data.
"""
from collections.abc import Sequence

from traits.api import Instance, List, observe
from traits.observation.api import trait

from pyface.data_view.abstract_data_model import (
    AbstractDataModel, DataViewSetError
)
from pyface.data_view.index_manager import IntIndexManager
from pyface.data_view.data_models.data_accessors import AbstractDataAccessor


class RowTableDataModel(AbstractDataModel):
    """ A data model that presents a sequence of objects as rows.

    The data is expected to be a sequence of row objects, each object
    providing values for the columns via an AbstractDataAccessor subclass.
    Concrete implementations can be found in the data_accessors module that
    get data from attributes, indices of sequences, and keys of mappings,
    but for more complex situations, custom accessors can be defined.
    """

    #: A sequence of objects to display as rows.
    data = Instance(Sequence, allow_none=False)

    #: An object which describes how to map data for the row headers.
    row_header_data = Instance(AbstractDataAccessor, allow_none=False)

    #: An object which describes how to map data for each column.
    column_data = List(Instance(AbstractDataAccessor, allow_none=False))

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(IntIndexManager, args=(), allow_none=False)

    # Data structure methods

    def get_column_count(self):
        """ How many columns in the data view model.

        Returns
        -------
        column_count : non-negative int
            The number of columns that the data view provides.
        """
        return len(self.column_data)

    def can_have_children(self, row):
        """ Whether or not a row can have child rows.

        Only the root has children.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.

        Returns
        -------
        can_have_children : bool
            Whether or not the row can ever have child rows.
        """
        return len(row) == 0

    def get_row_count(self, row):
        """ How many child rows the row currently has.

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
            return len(self.data)
        else:
            return 0

    # Data value methods

    def get_value(self, row, column):
        """ Return the Python value for the row and column.

        This uses the row_header_data and column_data accessors to extract
        values for the row and column.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        value : Any
            The value represented by the given row and column.
        """
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        if len(row) == 0:
            return column_data.title
        obj = self.data[row[0]]
        return column_data.get_value(obj)

    def can_set_value(self, row, column):
        """ Whether the value in the indicated row and column can be set.

        This uses the row_header_data and column_data accessors to determine
        if the value may be changed.

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
        if len(row) == 0:
            return False
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        obj = self.data[row[0]]
        return column_data.can_set_value(obj)

    def set_value(self, row, column, value):
        """ Set the Python value for the row and column.

        This uses the row_header_data and column_data accessors to set
        the value.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.
        value : Any
            The new value for the given row and column.

        Raises
        -------
        DataViewSetError
            If the value cannot be set.
        """
        if len(row) == 0:
            raise DataViewSetError("Can't set column titles.")
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        obj = self.data[row[0]]
        column_data.set_value(obj, value)
        self.values_changed = (row, column, row, column)

    def get_value_type(self, row, column):
        """ Return the value type of the given row and column.

        This uses the row_header_data and column_data accessors to get
        the value type.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 0 or 1.

        Returns
        -------
        value_type : AbstractValueType or None
            The value type of the given row and column, or None if no value
            should be displayed.
        """
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        if len(row) == 0:
            return column_data.title_type
        return column_data.value_type

    # data update methods

    @observe("data")
    def _update_data(self, event):
        self.structure_changed = True

    @observe(trait("data", notify=False).list_items(optional=True))
    def _update_data_items(self, event):
        if len(event.added) != len(event.removed):
            # number of rows has changed
            self.structure_changed = True
        else:
            if isinstance(event.index, int):
                start = event.index
                stop = min(event.index + len(event.added), len(self.data)) - 1
            else:
                start = event.index.start
                stop = min(event.index.stop, len(self.data)) - 1
            self.values_changed = ((start,), (), (stop,), ())

    @observe('row_header_data')
    def _update_row_header_data(self, event):
        self.values_changed = ((), (), (), ())

    @observe('row_header_data:updated')
    def _update_row_header_data_event(self, event):
        if event.new[1] == 'value':
            if len(self.data) > 0:
                self.values_changed = ((0,), (), (len(self.data) - 1,), ())
        else:
            self.values_changed = ((), (), (), ())

    @observe('column_data.items')
    def _update_all_column_data_items(self, event):
        self.structure_changed = True

    @observe('column_data:items:updated')
    def _update_column_data(self, event):
        index = self.column_data.index(event.new[0])
        if event.new[1] == 'value':
            if len(self.data) > 0:
                self.values_changed = (
                    (0,), (index,), (len(self.data) - 1,), (index,)
                )
        else:
            self.values_changed = ((), (index,), (), (index,))

    # default data value

    def _data_default(self):
        return []
