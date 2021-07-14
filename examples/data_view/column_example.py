# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Example showing DataView for ColumnDataModel using row info. """

import logging

from traits.api import Bool, Dict, HasStrictTraits, Instance, Int, Str, List

from pyface.api import ApplicationWindow, GUI, Image, ImageResource
from pyface.data_view.api import (
    DataViewWidget, IDataViewWidget, table_format, csv_format
)
from pyface.data_view.exporters.api import RowExporter
from pyface.data_view.value_types.api import (
    BoolValue, ColorValue, IntValue, TextValue, no_value
)
from pyface.ui_traits import PyfaceColor

from column_data_model import (
    AbstractRowInfo, ColumnDataModel, HasTraitsRowInfo
)
from example_data import (
    any_name, family_name, favorite_color, age, street, city, country
)

logger = logging.getLogger(__name__)


flags = {
    'Canada': ImageResource('ca.png'),
    'UK': ImageResource('gb.png'),
    'USA': ImageResource('us.png'),
}


class Address(HasStrictTraits):

    street = Str()

    city = Str()

    country = Str()


class Person(HasStrictTraits):

    name = Str()

    age = Int()

    favorite_color = PyfaceColor()

    contacted = Bool()

    address = Instance(Address)


class CountryValue(TextValue):

    flags = Dict(Str, Image, update_value_type=True)

    def has_image(self, model, row, column):
        value = model.get_value(row, column)
        return value in self.flags

    def get_image(self, model, row, column):
        value = model.get_value(row, column)
        return self.flags[value]


row_info = HasTraitsRowInfo(
    title='People',
    value='name',
    value_type=TextValue(),
    rows=[
        HasTraitsRowInfo(
            title="Age",
            value="age",
            value_type=IntValue(minimum=0),
        ),
        HasTraitsRowInfo(
            title="Favorite Color",
            value="favorite_color",
            value_type=ColorValue(),
        ),
        HasTraitsRowInfo(
            title="Contacted",
            value="contacted",
            value_type=BoolValue(true_text="Yes", false_text="No"),
        ),
        HasTraitsRowInfo(
            title="Address",
            value_type=no_value,
            value='address',
            rows=[
                HasTraitsRowInfo(
                    title="Street",
                    value="address.street",
                    value_type=TextValue(),
                ),
                HasTraitsRowInfo(
                    title="City",
                    value="address.city",
                    value_type=TextValue(),
                ),
                HasTraitsRowInfo(
                    title="Country",
                    value="address.country",
                    value_type=CountryValue(flags=flags),
                ),
            ],
        ),
    ],
)


class MainWindow(ApplicationWindow):
    """ The main application window. """

    data = List(Instance(Person))

    row_info = Instance(AbstractRowInfo)

    data_view = Instance(IDataViewWidget)

    def _create_contents(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self.data_view = DataViewWidget(
            parent=parent,
            data_model=ColumnDataModel(
                data=self.data,
                row_info=self.row_info,
            ),
            selection_mode='extended',
            exporters=[
                RowExporter(
                    format=table_format,
                    column_headers=True,
                    row_headers=True,
                ),
                RowExporter(
                    format=csv_format,
                    column_headers=True,
                ),
            ]
        )
        self.data_view._create()
        return self.data_view.control

    def _data_default(self):
        logger.info("Initializing data")
        people = [
            Person(
                name='%s %s' % (any_name(), family_name()),
                age=age(),
                favorite_color=favorite_color(),
                address=Address(
                    street=street(),
                    city=city(),
                    country=country(),
                ),
            )
            for i in range(100)
        ]
        logger.info("Data initialized")
        return people

    def destroy(self):
        self.data_view.destroy()
        super().destroy()


# Application entry point.
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow(row_info=row_info)
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
    logger.info("Shutting down")
