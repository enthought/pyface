import enum
from functools import partial
import itertools
import logging

from traits.api import (
    Any, Bool, Event, List, Instance, HasStrictTraits, Dict, Callable, observe,
    Property, Str
)

from pyface.api import ApplicationWindow, GUI

from pyface.color import Color
from pyface.data_view.api import DataViewSetError, DataViewGetError
from pyface.data_view.abstract_value_type import CheckState
from pyface.data_view.data_models.data_accessors import AttributeDataAccessor
from pyface.data_view.data_models.row_table_data_model import RowTableDataModel
from pyface.fields.api import ComboField

# Use Qt implementations for proof-of-concept purposes.
from pyface.qt import is_qt5
from pyface.qt.QtCore import Qt
from pyface.qt.QtGui import (
    QColor, QStyledItemDelegate, QTextEdit, QComboBox,
)
from pyface.ui.qt4.data_view.data_view_item_model import DataViewItemModel
from pyface.ui.qt4.data_view.data_view_widget import DataViewWidget


logger = logging.getLogger(__name__)


class NewDataModel(RowTableDataModel):
    """ A model for the data structure.

    In Qt world, this maps to a QAbstractItemModel.

    It is responsible for the getting and setting of data values.
    """

    def get_value_type(self, row, column):
        raise RuntimeError("Remove value type from model.")

    def get_data_accessor(self, row, column):
        """ Return the AbstractDataAccessor used for the given row and column.
        """
        if len(column) == 0:
            return self.row_header_data
        else:
            return self.column_data[column[0]]


class Handle(HasStrictTraits):
    """ This is an object given to an BaseItemEditor for getting and
    setting values.
    """

    value = Property()

    _model = Any()

    _row = Any()

    _column = Any()

    _delegate = Any()

    def __init__(self, *, model, row, column, delegate):
        super().__init__()
        self._model = model
        self._row = row
        self._column = column
        self._delegate = delegate

    def _get_value(self):
        return self._model.get_value(self._row, self._column)

    def _set_value(self, value):
        if not self._delegate.validator(value):
            return
        self._model.set_value(self._row, self._column, value)


class BaseItemEditor(HasStrictTraits):

    editing_finished = Event()

    handle = Instance(Handle)

    def create(self, parent):
        raise NotImplementedError("This method must return a widget control.")


class TraitsUIEditorItemEditor(BaseItemEditor):
    """ An implementation of a BaseItemEditor that allows any TraitsUI
    editor to be used as the item editor.
    """

    editor_factory = Any()

    style = Str("simple")

    def create(self, parent):
        from traitsui.api import UI, default_handler
        ui = UI(handler=default_handler())
        factory = getattr(self.editor_factory, self.style + "_editor")
        editor = factory(ui, self.handle, "value", "", parent)
        editor.prepare(parent)
        return editor.control


class ItemDelegate(HasStrictTraits):
    """ This replaces ValueType, and will play the role of providing
    custom renderer.

    In Qt world, this maps to QAbstractItemDelegate, plus the different
    handling to do with different role flags in the view.
    """

    # Callable(model, row, column) -> boolean
    is_delegate_for = Callable()

    # Callable(value) -> boolean
    # Note that the value has already been transformed back to the business
    # specifiv value as is found on the data model.
    validator = Callable(default_value=lambda value: True)

    # Callable(any) -> str
    to_text = Callable(default_value=str, allow_none=True)

    # Callable(str) -> any
    from_text = Callable(default_value=None, allow_none=True)

    # Callable(any) -> CheckState
    to_check_state = Callable(default_value=None, allow_none=True)

    # Callable(CheckState) -> any
    from_check_state = Callable(default_value=None, allow_none=True)

    # Callable(any) -> Color
    to_bg_color = Callable(default_value=None, allow_none=True)

    # Callable(parent, Handle) -> ItemEditor
    item_editor_factory = Callable(default_value=None, allow_none=True)


class QtCustomItemDelegate(QStyledItemDelegate):
    """ Custom implementation of the QAbstractItemDelegate.

    It uses the item_editor_factory from the ItemDelegate object to create
    new editor.
    """

    def createEditor(self, parent, option, index):
        """ Reimplemented to return the editor for a given index."""

        item_model = index.model()
        row = item_model._to_row_index(index)
        column = item_model._to_column_index(index)
        data_model = item_model.model
        delegate = item_model._get_delegate(row, column)
        if delegate.item_editor_factory is not None:
            item_editor = delegate.item_editor_factory(
                handle=Handle(
                    model=data_model,
                    row=row,
                    column=column,
                    delegate=delegate,
                )
            )
            control = item_editor.create(parent)
            control.setFocusPolicy(Qt.StrongFocus)
            control.setAutoFillBackground(True)
            control.setParent(parent)
            return control

        return super().createEditor(parent, option, index)

    def updateEditorGeometry(self, editor, option, index):
        """ Update the editor's geometry.
        """
        editor.setGeometry(option.rect)


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

        if delegate.from_text is not None:
            flags |= Qt.ItemIsEditable

        if delegate.item_editor_factory is not None:
            flags |= Qt.ItemIsEditable

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

        if role == Qt.EditRole and delegate.to_text is not None:
            return delegate.to_text(value)

        if role == Qt.CheckStateRole and delegate.to_check_state is not None:
            return self.get_check_state_map[delegate.to_check_state(value)]

        if role == Qt.BackgroundRole and delegate.to_bg_color is not None:
            return delegate.to_bg_color(value).to_toolkit()

        if role == Qt.ForegroundRole and delegate.to_bg_color is not None:
            color = delegate.to_bg_color(value)
            return QColor(255, 255, 255) if color.is_dark else QColor(0, 0, 0)

        return None

    def setData(self, index, value, role=Qt.EditRole):
        """ Reimplemented setData to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)

        delegate = self._get_delegate(row, column)

        if role == Qt.EditRole and delegate.from_text is not None:
            return self._set_value_with_exception(
                row=row,
                column=column,
                value=value,
                mapper=delegate.from_text,
                validator=delegate.validator,
            )

        if role == Qt.CheckStateRole and delegate.from_check_state is not None:
            value = self.set_check_state_map[value]
            return self._set_value_with_exception(
                row=row,
                column=column,
                value=value,
                mapper=delegate.from_check_state,
                validator=delegate.validator,
            )

        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Reimplemented headerData to use delegates instead of ValueType."""
        if orientation == Qt.Horizontal:
            row = ()
            if section == 0:
                column = ()
            else:
                column = (section - 1,)
        else:
            # XXX not currently used, but here for symmetry and completeness
            row = (section,)
            column = ()

        delegate = self._get_delegate(row, column)
        value = self.model.get_value(row, column)
        if role == Qt.DisplayRole and delegate.to_text is not None:
            return delegate.to_text(value)
        return None

    # Private methods

    def _get_delegate(self, row, column):
        """ Find the delegate for the given row and column index."""
        for delegate in self.delegates:
            if delegate.is_delegate_for(self.model, row, column):
                return delegate
        return ItemDelegate()

    def _set_value_with_exception(self, row, column, value, mapper, validator):
        """ Set model value with exception handling.

        Returns
        -------
        is_successful : bool
            If setting the value was successful.
        """
        try:
            mapped_value = mapper(value)
            if not validator(mapped_value):
                return False
            self.model.set_value(row, column, mapped_value)
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


    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        control = super()._create_control(parent)
        control.setItemDelegate(QtCustomItemDelegate(control))
        return control


# --------------------------------------------------------------------
# The following setup is for manual testing this proof-of-concept.
# --------------------------------------------------------------------

class DataItem:

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


def bool_to_check_state(value):
    """ Basic mapping from value to CheckState."""
    if bool(value):
        return CheckState.CHECKED
    return CheckState.UNCHECKED


def check_state_to_bool(value):
    """ Basic mapping from CheckState back to bool."""
    return value == CheckState.CHECKED


def text_to_int(text):
    """ Cast text to int."""
    try:
        return int(text)
    except ValueError:
        raise DataViewSetError(
            "Can't evaluate value: {!r}".format(text)
        )


class MainWindow(ApplicationWindow):

    def _create_contents(self, parent):
        data_model, delegates = create_model_and_delegates()
        widget = NewDataViewWidget(
            parent=parent,
            data_model=data_model,
            delegates=delegates,
        )
        widget._create()
        return widget.control


def is_row_header(model, row, column):
    return row == ()


def is_column_header(model, row, column):
    return column == ()


def is_column_index(index):
    return lambda model, row, column: column == (index, )


def create_model_and_delegates():
    """ Return a DataModel and a list of ItemDelegate for the widget.

    Returns
    -------
    model : AbstractDataModel
    delegates : list of ItemDelegate
    """

    values = itertools.cycle(zip(
        ["Hello", "Hi", "Hey"],
        [1, 2, 3],
        [True, False, True],
        [Color.from_str("green"), Color.from_str("green"), Color.from_str("black")],
        ["green", "green", "black"],
    ))
    objects = [
        DataItem(*next(values))
        for _ in range(1000)
    ]
    column_data = [
        AttributeDataAccessor(
            attr="b",
        ),
        AttributeDataAccessor(
            attr="b",
        ),
        AttributeDataAccessor(
            attr="c",
        ),
        AttributeDataAccessor(
            attr="d",
        ),
        AttributeDataAccessor(
            attr="e",
        ),
    ]

    model = NewDataModel(
        data=objects,
        row_header_data=AttributeDataAccessor(
            attr='a',
        ),
        column_data=column_data,
    )

    # demonstrate using TraitsUI editor
    from traitsui.api import (
        EnumEditor, TextEditor, RangeEditor, ProgressEditor
    )

    delegates = [
        ItemDelegate(
            is_delegate_for=is_row_header,
            to_text=lambda value: "HEADER " + str(value)
        ),
        ItemDelegate(
            is_delegate_for=is_column_header,
            validator=lambda value: value.startswith("H"),
            from_text=lambda text: text,
            item_editor_factory=partial(
                TraitsUIEditorItemEditor,
                editor_factory=TextEditor(),
                style="custom",
            ),
        ),
        ItemDelegate(
            is_delegate_for=is_column_index(0),
            validator=lambda value: value < 100,
            item_editor_factory=partial(
                TraitsUIEditorItemEditor,
                editor_factory=RangeEditor(low=0, high=100),
            )
        ),
        ItemDelegate(
            is_delegate_for=is_column_index(1),
            validator=lambda value: value < 100,
            item_editor_factory=partial(
                TraitsUIEditorItemEditor,
                editor_factory=ProgressEditor(min=0, max=100),
            )
        ),
        ItemDelegate(
            is_delegate_for=(
                lambda model, row, column: (
                    model.get_data_accessor(row, column).attr == "c"
                )
            ),
            to_check_state=bool_to_check_state,
            from_check_state=check_state_to_bool,
        ),
        ItemDelegate(
            is_delegate_for=(
                lambda model, row, column: (
                    model.get_data_accessor(row, column).attr == "d"
                )
            ),
            to_bg_color=lambda value: value,
            to_text=lambda value: value.hex(),
        ),
        ItemDelegate(
            is_delegate_for=(
                lambda model, row, column: (
                    model.get_data_accessor(row, column).attr == "e"
                )
            ),
            item_editor_factory=partial(
                TraitsUIEditorItemEditor,
                # How are the allowed values going to react to changes
                # on the object?
                editor_factory=EnumEditor(
                    values=["green", "red", "black"],
                ),
            )
        ),
    ]

    return model, delegates


def run():
    window = MainWindow()
    window._create()
    window.show(True)
    window.open()
    GUI().start_event_loop()


if __name__ == "__main__":
    run()
