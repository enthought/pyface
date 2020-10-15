# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, Int, List

from pyface.data_view.api import AbstractDataModel, TupleIndexManager


class IndexDataModel(AbstractDataModel):
    """ A data model that displays the indices of the cell. """

    index_manager = Instance(TupleIndexManager, ())

    shape = List(Int, [2, 3, 4])

    def get_column_count(self):
        return self.shape[-1]

    def can_have_children(self, row):
        return len(row) < len(self.shape) - 1

    def get_row_count(self, row):
        if len(row) == len(self.shape) - 1:
            return 0
        else:
            return self.shape[len(row)]

    def get_value(self, row, column):
        return "{} {}".format(row, column)

    def get_value_type(self, row, column):
        return TextValue(is_editable=False)


if __name__ == '__main__':
    from pyface.api import ApplicationWindow, GUI
    from pyface.data_view.i_data_view_widget import IDataViewWidget
    from pyface.data_view.data_view_widget import DataViewWidget
    from pyface.data_view.value_types.api import TextValue

    class MainWindow(ApplicationWindow):
        """ The main application window. """

        data_view = Instance(IDataViewWidget)

        def _create_contents(self, parent):
            """ Creates the left hand side or top depending on the style. """

            self.data_view = DataViewWidget(
                parent=parent,
                data_model=IndexDataModel(),
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
    window.data_view.observe(print, "selection")

    # Start the GUI event loop!
    gui.start_event_loop()
