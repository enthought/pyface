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
Abstract Data Model
===================

This module provides an ABC for all data view data models.  This specifies
the API that the data view widgets expect, and which the underlying
data is adapted to by the concrete implementations.  Data models are intended
to be toolkit-independent
"""
from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Event, Instance

from .index_manager import AbstractIndexManager


class AbstractDataModel(ABCHasStrictTraits):
    """ Abstract base class for data models. """

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(AbstractIndexManager)

    #: Event fired when the structure of the data changes.
    structure_changed = Event()

    #: Event fired when value changes without changes to structure.
    values_changed = Event()

    #: Event fired when selection changes.
    selection = Event()

    # Data structure methods

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    # Data value methods

    @abstractmethod
    def get_value(self, row, column):
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
        raise NotImplementedError

    @abstractmethod
    def set_value(self, row, column, value):
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
        raise NotImplementedError

    # Data channels

    @abstractmethod
    def get_value_type(self, row, column):
        """ Return the text value for the row and column.

        The value type for column headers are returned by calling this method
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
        raise NotImplementedError

    def iter_rows(self, start=[]):
        """ Iterator that yields rows in preorder.

        Parameters
        ----------
        start : row index
            The row to start at.  The iterator will yeild the row and all
            child rows.

        Yields
        ------
        row_index
            The current row index.
        """
        yield start
        if self.can_have_children(start):
            for row in range(self.get_row_count(start)):
                yield from self.iter_rows(start + [row])

    def iter_items(self, start_row=[]):
        """ Iterator that yields rows and columns in preorder.

        Columns are iterated in order.

        Parameters
        ----------
        start : row index
            The row to start at.  The iterator will yeild the row and all
            child rows.

        Yields
        ------
        row_index, column_index
            The current row and column indices.
        """
        for row in self.iter_rows():
            if row != []:
                yield row, []
            for column in range(self.get_column_count(row)):
                yield row, [column]
