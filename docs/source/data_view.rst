Pyface DataViews
=================

The Pyface DataView API allows visualization of heirarchical and
non-heirarchical tabular data.

Data Models
-----------

Data to be viewed needs to be exposed to the DataView infrastructure by
creating a data model for it.  This is a class that implements the
interface of |AbstractDataModel|.

A data model for a dictionary could be implemented like this::

    class DictDataModel(AbstractDataModel):

        data = Dict

        index_manager = Instance(IntIndexManager, ())

The index manager is an ``IntIndexManager`` because the data is
non-heirarchical and this is more memory-efficient than the alternative
``TupleIndexManager``.

Data Structure
~~~~~~~~~~~~~~

The keys are displayed in the row headers, so each row has one column
displaying the value::

    def get_column_count(self, row):
        return 1

The data is non-heirarchical, so on the root has children and the number
of child rows of the root is the length of the dictionary::

    def can_have_children(self, row):
        if len(row) == 0:
            return True
        return False

    def get_row_count(self, row):
        if len(row) == 0:
            return len(self.data)
        return False

Data Values
~~~~~~~~~~~

To get the values of the data model, we need to find the apprpriate value
from the dictionary::

    keys_header = Str("Keys")
    values_header = Str("Values")

    def get_value(self, row, column):
        if len(row) == 0:
            # this is a column header
            if len(row) == 0:
                # title of the row headers
                return self.keys_header
            else:
                return self.values_header
        else:
            row_index = row[0]
            key, value = list(self.data.items())[row_index]
            if len(column) == 0:
                # the is a row header, so get the key
                return key
            else:
                return value

In this case, all of the values are text, and read-only, so we can have a
trait holding the value type, and return that for every item::

    header_value_type = Instance(AbstractValueType)
    key_value_type = Instance(AbstractValueType)
    value_type = Instance(AbstractValueType)

    def _default_header_value_type(self):
        return TextValue(is_editable=False)

    def _default_key_value_type(self):
        return TextValue(is_editable=False)

    def _default_value_type(self):
        return TextValue(is_editable=False)

    def get_value_type(self, row, column):
        if len(row) == 0:
            return self.header_value_type
        elif len(column) == 0:
            return self.key_value_type
        else:
            return self.value_type

The default assumes that values representable as text, but if the values were
ints, for example then the class could be instantiated with::

    model = DictDataModel(value_type=IntValue(is_editable=False))

The ``is_editable`` arguments are not strictly needed, as the default
implementation of |can_set_value| returns False, but if we wanted to make the
data model read-write we would need to write an implementation of
|can_set_value| which returns True for editable items, and an implementation
of |set_value| that updates the data in-place.  This would look something like::

    def can_set_value(self, row, column):
        return len(row) != 0 and len(column) != 0:

    def set_value(self, row, column, value):
        if len(row) == 0 or len(column) == 0:
            return False
        row_index = row[0]
        key = list(self.data)[row_index]
        self.data[key] = value
        return True

Update Events
-------------

Finally, when the underlying data changes, the DataView infrastructure expects
certain event traits to be fired.  If a value is changed, or the value type is
updated, but the number of rows and columns is unaffected, then the
``values_changed`` trait should be fired with a tuple of ``(start_row_index,
start_column_index, end_row_index, end_column_index)``.  If a major change has
occurred, or if the size, shape or layout of the data has changed, then
the ``structure_changed`` event should be fired with a simple ``True`` value.

So for example, if the value types change, only the displayed values need to be
updated::

    @observe('header_value_type.updated')
    def header_values_updated(self, event):
        self.values_changed = ([], [], [], [0])

    @observe('key_value_type.updated')
    def key_values_updated(self, event):
        self.values_changed = ([0], [], [len(self.data) - 1], [])

    @observe('value_type.updated')
    def values_updated(self, event):
        self.values_changed = ([0], [0], [len(self.data) - 1], [0])

On the other hand, if the dictionary or its items change, then it is simplest
to just indicate that the entire view needs updating::

    @observe('data.items')
    def data_updated(self, event):
        self.structure_changed = True



.. |AbstractDataModel| replace:: :py:class:`~pyface.data_view.abstract_data_model.AbstractDataModel`
.. |can_set_value| replace:: :py:class:`~pyface.data_view.abstract_data_model.AbstractDataModel.can_set_value`
.. |set_value| replace:: :py:class:`~pyface.data_view.abstract_data_model.AbstractDataModel.set_value`
