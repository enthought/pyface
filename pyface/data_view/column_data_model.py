from abc import abstractmethod

from traits.api import (
    ABCHasStrictTraits, Callable, HasTraits, Instance, List, Str
)
from traits.trait_base import xgetattr, xsetattr

from .abstract_data_model import AbstractDataModel
from .index_manager import TupleIndexManager


def id(obj):
    return obj


class AbstractRowInfo(ABCHasStrictTraits):
    """ Configuration for a data row in a ColumnDataModel.
    """

    #: The text to display in the first column.
    title = Str

    #: The child rows of this row, if any.
    rows = List(Instance('AbstractRowInfo'))

    #: The method to format the value as a string.
    format = Callable(str)

    #: The method to evaluate a string into a value.
    evaluate = Callable(id)

    @abstractmethod
    def get_value(self, obj):
        raise NotImplementedError

    def set_value(self, obj):
        return False

    def get_text(self, obj):
        value = self.get_value(obj)
        if value is None:
            return ''
        return self.format(value)

    def set_text(self, obj, text):
        return self.set_value(obj, self.evaluate(text))


class ObjectRowInfo(AbstractRowInfo):

    #: The extended trait name of the trait holding the value.
    value = Str

    def get_value(self, obj):
        return xgetattr(obj, self.value, None)

    def set_value(self, obj, value):
        xsetattr(obj, self.value, value)
        return True


class DictRowInfo(AbstractRowInfo):

    #: The extended trait name of the dictionary holding the values.
    value = Str

    #: The key holding the value.
    key = Str

    def get_value(self, obj):
        data = xgetattr(obj, self.value, None)
        return data.get(self.key, None)

    def set_value(self, obj, value):
        data = xgetattr(obj, self.value, None)
        data[self.key] = value
        return True


class ColumnDataModel(AbstractDataModel):

    #: A list of objects to display in columns.
    data = List(Instance(HasTraits))

    #: An object which describes how to map data for each row.
    row_info = Instance(AbstractRowInfo)

    #: The index manager that helps convert toolkit indices to data view
    #: indices.
    index_manager = Instance(TupleIndexManager, ())

    def get_column_count(self, row):
        return len(self.data) + 1

    def can_have_children(self, row):
        if not row:
            return True
        row_info = self._row_info_object(row)
        return len(row_info.rows) != 0

    def get_row_count(self, row):
        row_info = self._row_info_object(row)
        return len(row_info.rows)

    def get_value(self, row, column):
        row_info = self._row_info_object(row)
        if column[0] == 0:
            return row_info.title
        obj = self.data[column[0]-1]
        return row_info.get_value(obj)

    def set_value(self, row, column, value):
        row_info = self._row_info_object(row)
        if column[0] == 0:
            return False
        obj = self.data[column[0]-1]
        return row_info.set_value(obj, value)

    def get_text(self, row, column):
        row_info = self._row_info_object(row)
        if column[0] == 0:
            return row_info.title
        obj = self.data[column[0]-1]
        return row_info.get_text(obj)

    def set_text(self, row, column, text):
        row_info = self._row_info_object(row)
        if column[0] == 0:
            return False
        obj = self.data[column[0]-1]
        return row_info.set_value(obj, text)

    def _row_info_object(self, row):
        row_info = self.row_info
        for index in row:
            row_info = row_info.rows[index]
        return row_info
