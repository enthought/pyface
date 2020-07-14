# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Array, Instance

from pyface.api import ApplicationWindow, GUI
from pyface.data_view.data_models.array_data_model import ArrayDataModel
from pyface.data_view.i_data_view_widget import IDataViewWidget
from pyface.data_view.data_view_widget import DataViewWidget
from pyface.data_view.value_types.api import FloatValue


class MainWindow(ApplicationWindow):
    """ The main application window. """

    data = Array()

    data_view = Instance(IDataViewWidget)

    def _create_contents(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self.data_view = DataViewWidget(
            parent=parent,
            data_model=ArrayDataModel(
                data=self.data,
                value_type=FloatValue(),
            ),
        )
        self.data_view._create()
        return self.data_view.control

    def _data_default(self):
        import numpy
        return numpy.random.uniform(size=(10000, 10, 10))*1000000

    def destroy(self):
        self.data_view.destroy()
        super().destroy()


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
