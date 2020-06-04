from traits.api import Array, Instance

from pyface.api import ApplicationWindow, GUI
from pyface.data_view.array_data_model import ArrayDataModel
from pyface.data_view.i_data_view_widget import IDataViewWidget
from pyface.data_view.data_view_widget import DataViewWidget


class MainWindow(ApplicationWindow):
    """ The main application window. """

    data = Array

    data_view = Instance(IDataViewWidget)

    def _create_contents(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self.data_view = DataViewWidget(
            parent=parent,
            data_model=ArrayDataModel(data=self.data),
            #header_visible=False,
        )
        self.data_view._create()
        return self.data_view.control

    def _data_default(self):
        import numpy
        return numpy.random.uniform(size=(100000, 10))


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
