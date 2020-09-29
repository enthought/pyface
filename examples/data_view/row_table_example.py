# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import HasStrictTraits, Instance, Int, Str, List

from pyface.api import ApplicationWindow, GUI
from pyface.data_view.data_models.data_accessors import AttributeDataAccessor
from pyface.data_view.data_models.row_table_data_model import (
    RowTableDataModel
)
from pyface.data_view.data_view_widget import DataViewWidget
from pyface.data_view.i_data_view_widget import IDataViewWidget
from pyface.data_view.value_types.api import ConstantValue, IntValue, TextValue

from example_data import any_name, family_name, age, street, city, country


# The data model

class Address(HasStrictTraits):

    street = Str()

    city = Str()

    country = Str()


class Person(HasStrictTraits):

    name = Str()

    age = Int()

    address = Instance(Address, ())


row_header_data = AttributeDataAccessor(
    title='People',
    attr='name',
    value_type=TextValue(),
)

column_data = [
    AttributeDataAccessor(
        attr="age",
        value_type=IntValue(minimum=0),
    ),
    AttributeDataAccessor(
        attr="address.street",
        value_type=TextValue(),
    ),
    AttributeDataAccessor(
        attr="address.city",
        value_type=TextValue(),
    ),
    AttributeDataAccessor(
        attr="address.country",
        value_type=TextValue(),
    ),
]


class MainWindow(ApplicationWindow):
    """ The main application window. """

    #: A collection of People.
    data = List(Instance(Person))

    #: The data view widget.
    data_view = Instance(IDataViewWidget)

    def _create_contents(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self.data_view = DataViewWidget(
            parent=parent,
            data_model=RowTableDataModel(
                data=self.data,
                row_header_data=row_header_data,
                column_data=column_data
            ),
        )
        self.data_view._create()
        return self.data_view.control

    def _data_default(self):
        people = [
            Person(
                name='%s %s' % (any_name(), family_name()),
                age=age(),
                address=Address(
                    street=street(),
                    city=city(),
                    country=country(),
                ),
            )
            for i in range(100000)
        ]
        return people

    def destroy(self):
        self.data_view.destroy()
        super().destroy()


if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()
