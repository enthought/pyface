# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from abc import abstractmethod

from traits.api import (
    ABCHasStrictTraits, ComparisonMode, Event, HasTraits, Instance,
    List, Str, observe
)
from traits.trait_base import xgetattr, xsetattr

from pyface.data_view.api import (
    AbstractDataModel, AbstractValueType, DataViewSetError, TupleIndexManager
)
from pyface.data_view.value_types.api import TextValue


class AbstractRowInfo(ABCHasStrictTraits):
    """ Configuration for a data row in a ColumnDataModel.
    """

    #: The text to display in the first column.
    title = Str()

    #: The child rows of this row, if any.
    rows = List(
        Instance('AbstractRowInfo'),
        comparison_mode=ComparisonMode.identity,
    )

    #: The value type of the data stored in this row.
    title_type = Instance(
        AbstractValueType,
        factory=TextValue,
        kw={'is_editable': False},
    )

    #: The value type of the data stored in this row.
    value_type = Instance(AbstractValueType)

    #: An event fired when the row or its children update.  The payload is
    #: a tuple of whether the title or value changed (or both), and the
    #: row_index affected.
    updated = Event

    def __iter__(self):
        yield self
        for row in self.rows:
            yield from row

    @abstractmethod
    def get_value(self, obj):
        raise NotImplementedError()

    @abstractmethod
    def can_set_value(self, obj):
        raise NotImplementedError()

    def set_value(self, obj):
        return

    @abstractmethod
    def get_observable(self, obj):
        raise NotImplementedError()

    # trait observers

    @observe('title,title_type.updated')
    def title_updated(self, event):
        self.updated = (self, 'title', [])

    @observe('value_type.updated')
    def value_type_updated(self, event):
        self.updated = (self, 'value', [])

    @observe('rows.items')
    def rows_updated(self, event):
        self.updated = (self, 'rows', [])

    @observe('rows:items:updated')
    def row_item_updated(self, event):
        row = event.object
        row_info, part, row_index = event.new
        row_index = [self.rows.index(row)] + row_index
        self.updated = (row_info, part, row_index)


class HasTraitsRowInfo(AbstractRowInfo):
    """ RowInfo that presents a named trait value.
    """

    #: The extended trait name of the trait holding the value.
    value = Str()

    def get_value(self, obj):
        return xgetattr(obj, self.value, None)

    def can_set_value(self, obj):
        return self.value != ''

    def set_value(self, obj, value):
        if not self.value:
            return
        xsetattr(obj, self.value, value)

    def get_observable(self):
        return self.value

    @observe('value')
    def value_type_updated(self, event):
        self.updated = (self, 'value', [])


class DictRowInfo(AbstractRowInfo):
    """ RowInfo that presents an item in a dictionary.

    The attribute ``value`` should reference a dictionary trait on a
    has traits object.
    """

    #: The extended trait name of the dictionary holding the values.
    value = Str()

    #: The key holding the value.
    key = Str()

    def get_value(self, obj):
        data = xgetattr(obj, self.value, None)
        return data.get(self.key, None)

    def can_set_value(self, obj):
        return self.value != ''

    def set_value(self, obj, value):
        data = xgetattr(obj, self.value, None)
        data[self.key] = value

    def get_observable(self):
        return self.value + '.items'

    @observe('value,key')
    def value_type_updated(self, event):
        self.updated = (self, 'value', [])


class ColumnDataModel(AbstractDataModel):
    """ A data model that presents a list of objects as columns.
    """

    #: A list of objects to display in columns.
    data = List(
        Instance(HasTraits),
        comparison_mode=ComparisonMode.identity,
    )

    #: An object which describes how to map data for each row.
    row_info = Instance(AbstractRowInfo)

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(TupleIndexManager, args=())

    def get_column_count(self):
        return len(self.data)

    def can_have_children(self, row):
        if len(row) == 0:
            return True
        row_info = self._row_info_object(row)
        return len(row_info.rows) != 0

    def get_row_count(self, row):
        row_info = self._row_info_object(row)
        return len(row_info.rows)

    def get_value(self, row, column):
        row_info = self._row_info_object(row)
        if len(column) == 0:
            return row_info.title
        obj = self.data[column[0]]
        return row_info.get_value(obj)

    def can_set_value(self, row, column):
        """ Whether the value in the indicated row and column can be set.

        This returns False for row headers, but True for all other values.

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
        if len(column) == 0:
            return False
        else:
            return True

    def set_value(self, row, column, value):
        row_info = self._row_info_object(row)
        if len(column) == 0:
            raise DataViewSetError("Cannot set value for row header.")
        obj = self.data[column[0]]
        row_info.set_value(obj, value)

    def get_value_type(self, row, column):
        row_info = self._row_info_object(row)
        if len(column) == 0:
            return row_info.title_type
        else:
            return row_info.value_type

    def _row_info_object(self, row):
        row_info = self.row_info
        for index in row:
            row_info = row_info.rows[index]
        return row_info
