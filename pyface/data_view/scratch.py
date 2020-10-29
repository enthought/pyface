
from traits.api import HasStrictTraits

from pyface.api import ApplicationWindow, GUI

from pyface.data_view.data_models.data_accessors import AttributeDataAccessor
from pyface.data_view.data_models.row_table_data_model import RowTableDataModel

from pyface.data_view.value_types.api import TextValue   # placeholder for now.

# Use Qt implementations for proof-of-concept purposes.
from pyface.ui.qt4.data_view.data_view_item_model import DataViewItemModel
from pyface.ui.qt4.data_view.data_view_widget import DataViewWidget



class DataItem:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class NewDataModel(RowTableDataModel):
    """ A model for the data structure.
    In Qt world, this maps to a QAbstractItemModel.
    """

    def get_value_type(self, row, column):
        # raise RuntimeError("Remove value type from model.")
        return TextValue()


class ValueDelegate(HasStrictTraits):
    """ This replaces ValueType, and will play the role of providing
    custom renderer.

    In Qt world, this maps to QAbstractItemDelegate, plus the different
    handling to do with different role flags in the view.
    """
    pass


class NewDataViewItemModel(DataViewItemModel):
    """ Override functionality of DataViewItemModel."""
    pass


class NewDataViewWidget(DataViewWidget):
    """ Override to provide a different DataViewItemModel."""

    def _create_item_model(self):
        self._item_model = NewDataViewItemModel(
            self.data_model,
            self.selection_type,
            self.exporters,
        )


class MainWindow(ApplicationWindow):

    def _create_contents(self, parent):
        widget = NewDataViewWidget(
            parent=parent,
            data_model=create_model(),
        )
        widget._create()
        return widget.control


def create_model():
    objects = [
        DataItem(
            a="Hello", b="World", c=3,
        ),
        DataItem(
            a=2, b=3, c=4,
        ),
        DataItem(
            a=2, b=3, c=4,
        ),
    ]
    column_data = [
        AttributeDataAccessor(
            attr="b",
        ),
        AttributeDataAccessor(
            attr="c",
        ),
    ]
    return NewDataModel(
        data=objects,
        row_header_data = AttributeDataAccessor(
            title='People',
            attr='a',
        ),
        column_data=column_data,
    )


def run():
    window = MainWindow()
    window._create()
    window.show(True)
    window.open()
    GUI().start_event_loop()


if __name__ == "__main__":
    run()
