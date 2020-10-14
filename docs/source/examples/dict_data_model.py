# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import ComparisonMode, Dict, Instance, Str, observe

from pyface.data_view.api import (
    AbstractDataModel, AbstractValueType, DataViewSetError, IntIndexManager
)


class DictDataModel(AbstractDataModel):
    """ A data model that provides data from a dictionary. """

    #: The dictionary containing the data.
    data = Dict(comparison_mode=ComparisonMode.identity)

    #: The index manager.  Because the data is flat, we use the
    #: IntIndexManager.
    index_manager = Instance(IntIndexManager, ())

    #: The text to display in the key column header.
    keys_header = Str("Keys")

    #: The text to display in the values column header.
    values_header = Str("Values")

    #: The header data channels.
    header_value_type = Instance(AbstractValueType)

    #: The key column data channels.
    key_value_type = Instance(AbstractValueType)

    #: The value column data channels.
    value_type = Instance(AbstractValueType)

    def get_column_count(self):
        return 1

    def can_have_children(self, row):
        return len(row) == 0

    def get_row_count(self, row):
        if len(row) == 0:
            return len(self.data)
        return 0

    def get_value(self, row, column):
        if len(row) == 0:
            # this is a column header
            if len(column) == 0:
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

    def get_value_type(self, row, column):
        if len(row) == 0:
            return self.header_value_type
        elif len(column) == 0:
            return self.key_value_type
        else:
            return self.value_type

    def can_set_value(self, row, column):
        return len(row) != 0 and len(column) != 0

    def set_value(self, row, column, value):
        if self.can_set_value(row, column):
            row_index = row[0]
            key = list(self.data)[row_index]
            self.data[key] = value
        else:
            raise DataViewSetError()

    @observe('header_value_type.updated')
    def header_values_updated(self, event):
        self.values_changed = ([], [], [], [0])

    @observe('key_value_type.updated')
    def key_values_updated(self, event):
        self.values_changed = ([0], [], [len(self.data) - 1], [])

    @observe('value_type.updated')
    def values_updated(self, event):
        self.values_changed = ([0], [0], [len(self.data) - 1], [0])

    @observe('data.items')
    def data_updated(self, event):
        self.structure_changed = True

    def _header_value_type_default(self):
        return TextValue(is_editable=False)

    def _key_value_type_default(self):
        return TextValue(is_editable=False)

    def _value_type_default(self):
        return TextValue(is_editable=False)


if __name__ == '__main__':
    from pyface.api import ApplicationWindow, GUI
    from pyface.data_view.i_data_view_widget import IDataViewWidget
    from pyface.data_view.data_view_widget import DataViewWidget
    from pyface.data_view.value_types.api import IntValue, TextValue

    class MainWindow(ApplicationWindow):
        """ The main application window. """

        data_view = Instance(IDataViewWidget)

        def _create_contents(self, parent):
            """ Creates the left hand side or top depending on the style. """

            self.data_view = DataViewWidget(
                parent=parent,
                data_model=DictDataModel(
                    data={'one': 1, 'two': 2, 'three': 3},
                    value_type=IntValue(),
                ),
            )
            self.data_view._create()
            return self.data_view.control

        def destroy(self):
            self.data_view.destroy()
            super().destroy()

    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
