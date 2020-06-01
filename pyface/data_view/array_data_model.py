# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Array Data Model
================

This module provides an a concrete implementation of a data model for a 2D
numpy array.
"""
from traits.api import Array, Instance, observe

from .abstract_data_model import AbstractDataModel
from .index_manager import IntIndexManager


class ArrayDataModel(AbstractDataModel):

    #: The array being displayed.
    data = Array(shape=(None, None))

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(IntIndexManager, ())

    # Data structure methods

    def get_column_count(self, row):
        """ How many columns in the row of the data view model.

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
        if row == []:
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
        if row == []:
            return self.data.shape[0]
        return 0

    # Data value methods

    def get_value(self, row, column):
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
        if row == []:
            return column[0]
        elif column == []:
            # XXX not currently used
            return row[0]
        else:
            return self.data[row[0], column[0]]

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
        if row == []:
            return False
        elif column == []:
            # XXX not used
            return False
        else:
            self.data[row[0], column[0]] = value
            self.values_changed = ((row, column), (row, column))
            return True

    def get_text(self, row, column):
        """ Set the Python value for the row and column.

        The values for column headers can be set by calling this method
        with row as Root.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 1.
        value : any
            The new value for the given row and column.

        Returns
        -------
        success : bool
            Whether or not the value was set successfully.
        """
        return str(self.get_value(row, column))

    def set_text(self, row, column, text):
        """ Return the text value for the row and column.

        The text for column headers are returned by calling this method
        with row as Root.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 1.

        Returns
        -------
        text : str
            The text to display in the given row and column.
        """
        try:
            value = self.data.dtype.type(text.strip())
        except ValueError:
            return False
        return self.set_value(row, column, value)

    def get_style(self, row, column):
        """ Set the text value for the row and column.

        The text for column headers can be set by calling this method
        with row as Root.

        Parameters
        ----------
        row : sequence of int
            The indices of the row as a sequence from root to leaf.
        column : sequence of int
            The indices of the column as a sequence of length 1.
        text : str
            The new text value for the given row and column.

        Returns
        -------
        success : bool
            Whether or not the value was set successfully.
        """
        raise NotImplementedError

    # data update methods

    @observe('data', dispatch='ui')
    def data_updated(self, event):
        """ Handle the array being replaced with a new array. """
        if event.new.shape == event.old.shape:
            self.values_changed = (
                ([0], [0]),
                ([event.old.shape[0]], [event.old.shape[1]]),
            )
        else:
            self.structure_changed = True
