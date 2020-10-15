# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Example showing DataView for ArrayDataModel. """

import logging

import numpy as np

from traits.api import Array, Instance, observe

from pyface.api import ApplicationWindow, GUI
from pyface.data_view.api import (
    DataViewWidget, IDataViewWidget, table_format, csv_format, npy_format
)
from pyface.data_view.data_models.api import ArrayDataModel
from pyface.data_view.exporters.api import RowExporter
from pyface.data_view.value_types.api import FloatValue
from pyface.drop_handler import FileDropHandler


logger = logging.getLogger(__name__)


class MainWindow(ApplicationWindow):
    """ The main application window. """

    data = Array()

    data_view = Instance(IDataViewWidget)

    def load_data(self, path):
        try:
            self.data = np.load(path)
        except Exception:
            logger.exception()

    def _create_contents(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self.data_view = DataViewWidget(
            parent=parent,
            data_model=ArrayDataModel(
                data=self.data,
                value_type=FloatValue(),
            ),
            selection_mode='extended',
            exporters=[
                RowExporter(format=table_format),
                RowExporter(format=csv_format),
                RowExporter(format=npy_format),
            ],
            drop_handlers=[
                FileDropHandler(extensions=['.npy'], open_file=self.load_data),
            ],
        )
        self.data_view._create()
        return self.data_view.control

    def destroy(self):
        self.data_view.destroy()
        super().destroy()

    @observe('data')
    def _data_updated(self, event):
        if self.data_view is not None:
            self.data_view.data_model.data = self.data

    def _data_default(self):
        return np.random.uniform(size=(10000, 10, 10))*1000000


# Application entry point.
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
