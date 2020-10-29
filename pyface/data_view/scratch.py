import enum
import logging

from traits.api import Bool, List, Instance, HasStrictTraits, Dict, Callable

from pyface.api import ApplicationWindow, GUI


from pyface.data_view.api import DataViewSetError, DataViewGetError
from pyface.data_view.abstract_value_type import CheckState
from pyface.data_view.data_models.data_accessors import AttributeDataAccessor
from pyface.data_view.data_models.row_table_data_model import RowTableDataModel
from pyface.data_view.value_types.api import TextValue   # placeholder for now.

# Use Qt implementations for proof-of-concept purposes.
from pyface.qt import is_qt5
from pyface.qt.QtCore import Qt
from pyface.ui.qt4.data_view.data_view_item_model import DataViewItemModel
from pyface.ui.qt4.data_view.data_view_widget import DataViewWidget


logger = logging.getLogger(__name__)


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


class ItemDelegate(HasStrictTraits):
    """ This replaces ValueType, and will play the role of providing
    custom renderer.

    In Qt world, this maps to QAbstractItemDelegate, plus the different
    handling to do with different role flags in the view.
    """

    # Callable(model, row, column) -> boolean
    is_delegate_for = Callable()

    # Callable(any) -> str
    to_text = Callable(default_value=str, allow_none=True)

    # Callable(any) -> CheckState
    to_check_state = Callable(default_value=None, allow_none=True)

    # Callable(CheckState) -> any
    from_check_state = Callable(default_value=None, allow_none=True)


class NewDataViewItemModel(DataViewItemModel):
    """ Override functionality of Qt DataViewItemModel."""

    set_check_state_map = {
        Qt.Checked: CheckState.CHECKED,
        Qt.Unchecked: CheckState.UNCHECKED,
    }
    get_check_state_map = {
        CheckState.CHECKED: Qt.Checked,
        CheckState.UNCHECKED: Qt.Unchecked,
    }

    def __init__(
        self, model, selection_type, exporters, parent=None,
        delegates=None,
    ):
        """ Reimplemented to allow a list of delegates to be used by the
        model.
        """
        super().__init__(model, selection_type, exporters, parent)
        # The delegates include logic previously supported by ValueType.
        self.delegates = [] if delegates is None else delegates

    def flags(self, index):
        """ Reimplemented flags to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        if row == () and column == ():
            return Qt.ItemIsEnabled

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        if is_qt5 and not self.model.can_have_children(row):
            flags |= Qt.ItemNeverHasChildren

        delegate = self._get_delegate(row, column)
        if delegate.to_check_state is not None:
            flags |= Qt.ItemIsEditable
            flags |= Qt.ItemIsUserCheckable
        return flags

    def data(self, index, role=Qt.DisplayRole):
        """ Reimplemented data to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value = self.model.get_value(row, column)

        delegate = self._get_delegate(row, column)

        if role == Qt.DisplayRole and delegate.to_text is not None:
            return delegate.to_text(value)

        if role == Qt.CheckStateRole and delegate.to_check_state is not None:
            return self.get_check_state_map[delegate.to_check_state(value)]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        """ Reimplemented setData to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)

        delegate = self._get_delegate(row, column)

        if role == Qt.CheckStateRole and delegate.from_check_state is not None:
            value = self.set_check_state_map[value]
            return self._set_value_with_exception(
                row=row, column=column,
                value=delegate.from_check_state(value)
            )

        return False

    # Private methods

    def _get_delegate(self, row, column):
        """ Find the delegate for the given row and column index."""
        for delegate in self.delegates:
            if delegate.is_delegate_for(self.model, row, column):
                return delegate
        return ItemDelegate()

    def _set_value_with_exception(self, row, column, value):
        """ Set model value with exception handling.

        Returns
        -------
        is_successful : bool
            If setting the value was successful.
        """
        try:
            self.model.set_value(row, column, value)
        except DataViewSetError:
            return False
        except Exception:
            # unexpected error, log and persevere
            logger.exception(
                "setData failed: row %r, column %r, value %r",
                row,
                column,
                value,
            )
            return False
        else:
            return True


class NewDataViewWidget(DataViewWidget):
    """ Override to provide a different DataViewItemModel."""

    delegates = List(Instance(ItemDelegate))

    def _create_item_model(self):
        self._item_model = NewDataViewItemModel(
            self.data_model,
            self.selection_type,
            self.exporters,
            delegates=self.delegates,
        )


# --------------------------------------------------------------------
# The following setup is for manual testing this proof-of-concept.
# --------------------------------------------------------------------


def basic_to_check_state(value):
    if bool(value):
        return CheckState.CHECKED
    return CheckState.UNCHECKED


def basic_from_check_state(value):
    return value == CheckState.CHECKED


class MainWindow(ApplicationWindow):

    def _create_contents(self, parent):
        widget = NewDataViewWidget(
            parent=parent,
            data_model=create_model(),
            delegates=[
                ItemDelegate(
                    is_delegate_for=(
                        lambda model, row, column: column == (1, )
                    ),
                    to_check_state=basic_to_check_state,
                    from_check_state=basic_from_check_state,
                )
            ]
        )
        widget._create()
        return widget.control


def create_model():
    objects = [
        DataItem(
            a="Hello", b="World", c=True,
        ),
        DataItem(
            a=2, b=3, c=True,
        ),
        DataItem(
            a=2, b=3, c=True,
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
        row_header_data=AttributeDataAccessor(
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
