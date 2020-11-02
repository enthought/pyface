import enum
from functools import partial
import itertools
import logging

from traits.api import (
    Any, Bool, Event, List, Instance, HasStrictTraits, Dict, Callable, observe,
    Property, Str, Int, Enum
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


class ItemHandle(HasStrictTraits):
    """ This is an object given to delegates and item editors for
    displaying and editing item value.
    """

    # Proxy for accessing and modifying value on the data model.
    # This is particularly useful for custom editor because its changes can
    # be observed.
    value = Property()

    # Reference to the AbstractDataModel responsible for this item.
    model = Any()

    # Which row index this item refers to.
    row = Any()

    # Which column index this item refers to.
    column = Any()

    # ItemDelegate object used for this item.
    delegate = Any()

    def __init__(self, *, model, row, column, delegate):
        super().__init__()
        self.model = model
        self.row = row
        self.column = column
        self.delegate = delegate

    def _get_value(self):
        return self.model.get_value(self.row, self.column)

    def _set_value(self, value):
        """ Set model value with exception handling.

        Parameters
        ----------
        value : any
            Value to be set on the Model.
        """
        if not self.delegate.validator(self, value):
            return
        try:
            self.model.set_value(
                self.row, self.column, value
            )
        except DataViewSetError:
            pass


class BaseItemEditorFactory(HasStrictTraits):

    def create(self, parent, item_handle):
        """ Create the toolkit specific object as the custom editor.

        Parameters
        ----------
        parent : any
            Toolkit specific parent widget.
        item_handle : ItemHandle
            Handle for obtaining data from the data model as well as the
            row/column index this custom editor is referring to.

        Returns
        -------
        control : any
            Toolkit specific widget.
        """
        raise NotImplementedError("This method must return a widget control.")

    def commit(self, control, handle):
        """ Commit data at the end of an edit.

        If the user presses Escape to exit the edit mode, this method
        will not be called. If the user clicks outside of the editor or
        presses Tab (as long as it is not also captured by the editor), then
        this method is called to commit the data change.

        Default behaviour does nothing.

        Parameters
        ----------
        control : any
            Widget returned by ``create``.
        handle : ItemHandle
            Handle for commiting data. The commit action can be achieved by
            assigning value to ItemHandle.value.
        """
        pass

    def destroy(self, control):
        """ Implement how to dispose the control created.

        Note: This is not used in Qt4.

        If NotImplementedError is raised, the default behaviour is to
        destroy the control. Override this method to avoid the control
        being destroyed, or to do additional clean up before the control is
        destroyed.
        """
        raise NotImplementedError("No custom behaviour is implemented.")


class TraitsUIItemObject(HasStrictTraits):
    """ Object to hold the value being edited so that it does not immediately
    set on the data model. This delay effect only works when the editing occurs
    directly on the value, e.g. it would not work on InstanceEditor where the
    value is an object and the edited quantities are values on the object.
    """
    value = Any()


class TraitsUIItemEditorFactory(BaseItemEditorFactory):
    """ An implementation of a BaseItemEditorFactory that allows any TraitsUI
    editor to be used as the item editor.
    """

    # Editor factory for creating TraitsUI editor.
    editor_factory = Instance("traitsui.editor_factory.EditorFactory")

    # The style used on the factory. (sigh)
    style = Str("simple")

    # Callable to obtain the context for the TraitsUI editor.
    # e.g. populating this dictionary with a key 'key_name' pointing to
    # a HasTraits object allows 'key_name' to be used in the extended names.
    # e.g. ModelView adds 'model' to the context.
    # Callable(ItemHandle) -> dict
    context_getter = Callable(default_value=None, allow_none=None)

    def create(self, parent, item_handle):
        """ Reimplemented BaseItemEditorFactory.create to return a widget
        using TraitsUI editor.
        """
        from traitsui.api import UI, Handler

        holder_object = TraitsUIItemObject(value=item_handle.value)

        if self.context_getter is not None:
            context = self.context_getter(item_handle)
        else:
            context = {}

        ui = UI(handler=Handler(), context=context)

        factory = getattr(self.editor_factory, self.style + "_editor")
        editor = factory(ui, holder_object, "value", "", parent)
        editor.prepare(parent)
        editor.control.setParent(parent)

        # TraitsUI adds a cycle reference back to 'editor' in the control's
        # '_editor' attribute. This allows cleanup prior to object destruction
        # where the control object that gets passed back to destroy.
        return editor.control

    def commit(self, control, item_handle):
        """ Commit data at the end of an edit.

        Parameters
        ----------
        control : any
            Widget returned by create.
        item_handle : ItemHandle
            The commit action is achieved by assigning value to
            ItemHandle.value.
        """
        item_handle.value = control._editor.object.value

    def destroy(self, control):
        """ Implement how to dispose the control created.

        If NotImplementedError is raised, the default behaviour is to
        destroy the control. Override this method to avoid the control
        being destroyed, or to do additional clean up before the control is
        destroyed.
        """
        from traitsui.toolkit import toolkit
        control._editor.dispose()
        toolkit().destroy_control(control)


class ItemDelegate(HasStrictTraits):
    """ This absorbs the functionality of ValueType, and will play the role of
    providing custom renderer and editors.

    It does not map exactly to Qt's QAbstractItemDelegate, because for one
    QAbstractItemView, there is only one QAbstractItemDelegate, whose task
    is to manage display and editing of every item.

    This object is responsible for a subset of items only. The subset is
    defined by is_delegate_for.
    """

    # Callable(model, row, column) -> boolean
    is_delegate_for = Callable()

    # Callable(ItemHandle, value) -> boolean
    # Note that the value has already been transformed back to the business
    # specifiv value as is found on the data model.
    validator = Callable(default_value=lambda _, value: True)

    # Callable(ItemHandle, any) -> str
    to_text = Callable(
        default_value=lambda _, value: str(value), allow_none=True
    )

    # Callable(ItemHandle, str) -> any
    from_text = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, any) -> CheckState
    # This converts the value from the data model to a checkbox state and
    # enable the view of a checkbox next to an item. Note that checkbox
    # functionality is not supported in headers.
    to_check_state = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, CheckState) -> any
    # This converts the state of a checkbox in an item to a value the data
    # model understands. Note that checkbox functionality is not supported
    # in headers.
    from_check_state = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, any) -> Color
    to_bg_color = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, any) -> Color
    to_fg_color = Callable(allow_none=True)

    # Factory for creating custom editor.
    item_editor_factory = Instance(BaseItemEditorFactory, allow_none=True)

    def _to_fg_color_default(self):
        if self.to_bg_color is not None:

            def to_fg_color(item_handle, value):
                bg_color = self.to_bg_color(item_handle, value)
                if bg_color.is_dark:
                    return Color.from_str("white")
                return Color.from_str("black")

            return to_fg_color

        return None


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
            item_handle = item_model._get_handle_for_delegate(
                row, column, delegate
            )
            control = delegate.item_editor_factory.create(parent, item_handle)
            control.setFocusPolicy(Qt.StrongFocus)
            control.setAutoFillBackground(True)

            # This control is the 'editor' that gets passed back to this
            # QStyleItemDelegate.
            # These are NOT cycle references.
            control._item_handle = item_handle
            control._item_editor_factory = (
                delegate.item_editor_factory
            )
            return control

        return super().createEditor(parent, option, index)

    # The base class setEditorData is good enough.
    # The editor gets value from ItemHandle.value

    def setModelData(self, editor, model, index):
        """
        Parameters
        ----------
        editor : any
            Return value of createEditor
        model : QAbstractItemModel
            The item model that controls setting data.
        index : QModelIndex
            The index allowing access to the item model.
        """
        if hasattr(editor, "_item_handle"):
            # Created by the createEditor via the delegate.
            editor._item_editor_factory.commit(editor, editor._item_handle)
        else:
            # Not created by the delegate.
            super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        """ Update the editor's geometry.
        """
        rect = option.rect
        editor_size = editor.sizeHint()

        # This makes sure the editor can be seen, otherwise it
        # takes on the size of the cell, which could be too small.
        if rect.height() < editor_size.height():
            rect.setHeight(editor_size.height())
        if rect.width() < editor_size.width():
            rect.setWidth(editor_size.width())

        editor.setGeometry(rect)

    if is_qt5:

        def destroyEditor(self, editor, index):
            """ Override behaviour to do with destroying the editor
            """
            if hasattr(editor, "_item_editor_factory"):
                try:
                    editor._item_editor_factory.destroy(editor)
                except NotImplementedError:
                    super().destroyEditor(editor, index)
            else:
                # this simply calls editor.deleteLater
                super().destroyEditor(editor, index)

            self.sizeHintChanged.emit(index)


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

    def _get_handle_for_delegate(self, row, column, delegate):
        """ Create an instance of ItemHandle for delegates to use."""
        return ItemHandle(
            model=self.model,
            row=row,
            column=column,
            delegate=delegate,
        )

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

        if any((
                delegate.from_text is not None,
                delegate.item_editor_factory is not None,
                delegate.from_check_state is not None,
        )):
            flags |= Qt.ItemIsEditable

        if delegate.to_check_state is not None:
            flags |= Qt.ItemIsUserCheckable

        return flags

    def data(self, index, role=Qt.DisplayRole):
        """ Reimplemented data to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value = self.model.get_value(row, column)

        delegate = self._get_delegate(row, column)
        item_handle = self._get_handle_for_delegate(row, column, delegate)

        if role == Qt.DisplayRole and delegate.to_text is not None:
            return delegate.to_text(item_handle, value)

        if role == Qt.EditRole and delegate.to_text is not None:
            return delegate.to_text(item_handle, value)

        if role == Qt.CheckStateRole and delegate.to_check_state is not None:
            return self.get_check_state_map[
                delegate.to_check_state(item_handle, value)
            ]

        if role == Qt.BackgroundRole and delegate.to_bg_color is not None:
            return delegate.to_bg_color(item_handle, value).to_toolkit()

        if role == Qt.ForegroundRole and delegate.to_fg_color is not None:
            return delegate.to_fg_color(item_handle, value).to_toolkit()

        return None

    def setData(self, index, value, role=Qt.EditRole):
        """ Reimplemented setData to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)

        delegate = self._get_delegate(row, column)
        item_handle = self._get_handle_for_delegate(row, column, delegate)

        if (role == Qt.EditRole
                and isinstance(value, str)
                and delegate.from_text is not None):
            return self._set_value_with_exception(
                item_handle=item_handle,
                value=value,
                mapper=delegate.from_text,
            )

        if role == Qt.CheckStateRole and delegate.from_check_state is not None:
            value = self.set_check_state_map[value]
            return self._set_value_with_exception(
                item_handle=item_handle,
                value=value,
                mapper=delegate.from_check_state,
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
        item_handle = self._get_handle_for_delegate(row, column, delegate)
        value = self.model.get_value(row, column)
        if role == Qt.DisplayRole and delegate.to_text is not None:
            return delegate.to_text(item_handle, value)
        return None

    # Private methods

    def _get_delegate(self, row, column):
        """ Find the delegate for the given row and column index."""
        for delegate in self.delegates:
            if delegate.is_delegate_for(self.model, row, column):
                return delegate
        return ItemDelegate()

    def _set_value_with_exception(self, item_handle, value, mapper):
        """ Set model value with exception handling.

        Parameters
        ----------
        item_handle : ItemHandle
            Information to be passed back to the delegate for validation.
        value : any
            Value given to the item model before transformation.
        mapper : callable(item_handle, value)
            Transformer function to convert value before sending it to the
            data model.

        Returns
        -------
        is_successful : bool
            If setting the value was successful.
        """
        try:
            mapped_value = mapper(item_handle, value)
            if not item_handle.delegate.validator(item_handle, mapped_value):
                return False
            self.model.set_value(
                item_handle.row, item_handle.column, mapped_value
            )
        except DataViewSetError:
            return False
        except Exception:
            # unexpected error, log and persevere
            logger.exception(
                "setData failed: row %r, column %r, value %r",
                item_handle.row,
                item_handle.column,
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

        # Why are we limiting the height before???
        # With the sizeHintChanged signal in the item delegate, the row
        # can change size after editing.
        control.setUniformRowHeights(False)

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


def bool_to_check_state(item_handle, value):
    """ Basic mapping from value to CheckState."""
    if bool(value):
        return CheckState.CHECKED
    return CheckState.UNCHECKED


def check_state_to_bool(item_handle, value):
    """ Basic mapping from CheckState back to bool."""
    return value == CheckState.CHECKED


def text_to_int(item_handle, text):
    """ Cast text to int."""
    try:
        return int(text)
    except ValueError:
        raise DataViewSetError(
            "Can't evaluate value: {!r}".format(text)
        )


def validate_is_color_name(item_handle, text):
    try:
        Color.from_str(text)
    except Exception:
        return False
    else:
        return True


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
    return column == ()


def is_column_header(model, row, column):
    return row == ()


def is_column_index(index):
    return lambda model, row, column: column == (index, )


class Person(HasStrictTraits):

    name = Str()

    age = Int()

    favorite_bg_color = Enum(values="bg_color_choices")

    bg_color_choices = List(["red", "blue", "black"])

    favorite_fg_color = Enum(values="fg_color_choices")

    fg_color_choices = List(["yellow", "grey", "white"])

    greeting = Str("Hello")

    married = Bool()

    # FIXME: RowDataModel assumes each column must be accessing and modifying
    # a member of the object. If I want a cell for editing the whole object
    # (see use of InstanceEditor), I have to add this hook...
    _self = Property()

    def _set__self(self, value):
        pass

    def _get__self(self):
        return self


def create_model_and_delegates():
    """ Return a DataModel and a list of ItemDelegate for the widget.

    Returns
    -------
    model : AbstractDataModel
    delegates : list of ItemDelegate
    """

    names = itertools.cycle(["John", "Mary", "Peter"])
    bg_colors = itertools.cycle(["red", "blue", "black"])
    fg_colors = itertools.cycle(["yellow", "grey", "white"])
    objects = [
        Person(
            name=next(names),
            favorite_bg_color=next(bg_colors),
            favorite_fg_color=next(fg_colors),
        )
        for _ in range(1000)
    ]
    column_data = [
        AttributeDataAccessor(
            attr="age",
        ),
        AttributeDataAccessor(
            attr="age",
        ),
        AttributeDataAccessor(
            attr="married",
        ),
        AttributeDataAccessor(
            attr="favorite_bg_color",
        ),
        AttributeDataAccessor(
            attr="favorite_fg_color",
        ),
        # How else can the cell be used for editing the whole row?
        AttributeDataAccessor(
            attr="_self",
        ),
    ]

    model = NewDataModel(
        data=objects,
        row_header_data=AttributeDataAccessor(
            attr='greeting',
        ),
        column_data=column_data,
    )

    # demonstrate using TraitsUI editor
    from traitsui.api import (
        EnumEditor, TextEditor, RangeEditor, InstanceEditor
    )

    # Problem with the pattern of using a list of is_delegate_for:
    # It is easy to make mistakes and have two is_delegate_for returning
    # true for the same (row, column) index. The first one ends up being used
    # and the second one is silently ignored.
    # It is laborious and error-prone to maintain is_delegate_for when a new
    # column is added.
    # The first issue should be resolved by not using a list, but a
    # function that returns an ItemDelegate for the given (row, column) index.
    # The second issue should be resolved by having a front-facing function
    # that put together how to access value for a column and how to present
    # those values for that column.

    delegates = [
        # This shows customization of the header.
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_row_header(*args)
            ),
            to_text=lambda _, value: "multi-line text",
        ),
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_column_index(0)(*args)
            ),
            to_text=lambda _, value: "range editor",
        ),
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_column_index(1)(*args)
            ),
            to_text=lambda _, value: "not editable",
        ),
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_column_index(2)(*args)
            ),
            to_text=lambda _, value: "editable bool",
        ),
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_column_index(3)(*args)
            ),
            to_text=lambda _, value: "bg color",
        ),
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_column_index(4)(*args)
            ),
            to_text=lambda _, value: "fg color",
        ),
        ItemDelegate(
            is_delegate_for=lambda *args: (
                is_column_header(*args) and is_column_index(5)(*args)
            ),
            to_text=lambda _, value: "instance editor",
        ),
        # This shows using the custom multi-line text editor.
        # It also shows setting background colour not directly from the cell
        # value but from data related to the row.
        ItemDelegate(
            is_delegate_for=is_row_header,
            validator=lambda _, value: len(value) > 0,
            to_bg_color=lambda item_handle, _: (
                Color.from_str(item_handle.model.data[item_handle.row[0]].favorite_bg_color)
            ),
            to_fg_color=lambda item_handle, _: (
                Color.from_str(item_handle.model.data[item_handle.row[0]].favorite_fg_color)
            ),
            item_editor_factory=TraitsUIItemEditorFactory(
                editor_factory=TextEditor(),
                style="custom",
            ),
        ),
        # This shows using the RangeEditor as custom editor.
        ItemDelegate(
            is_delegate_for=lambda *args: (
                not is_column_header(*args) and is_column_index(0)(*args)
            ),
            validator=lambda _, value: value <= 100,
            item_editor_factory=TraitsUIItemEditorFactory(
                editor_factory=RangeEditor(low=0, high=100),
            )
        ),
        #
        #
        # The item for column index 1 is not defined, the default
        # is just ItemDelegate(), which is not editable.
        #
        #
        # This shows the checkbox along with editing text to be converted to
        # bool.
        ItemDelegate(
            is_delegate_for=lambda *args: (
                not is_column_header(*args) and is_column_index(2)(*args)
            ),
            to_check_state=bool_to_check_state,
            validator=lambda _, value: isinstance(value, bool),
            from_text=lambda _, value: (
                {"true": True, "false": False}.get(value.lower())
            ),
            from_check_state=check_state_to_bool,
        ),
        # This shows using EnumEditor and having the options dynamically
        # updated.
        ItemDelegate(
            is_delegate_for=lambda *args: (
                not is_column_header(*args) and is_column_index(3)(*args)
            ),
            item_editor_factory=TraitsUIItemEditorFactory(
                style="custom",
                editor_factory=EnumEditor(
                    mode="radio",
                    name="person.bg_color_choices",
                ),
                context_getter=lambda handle: (
                    {"person": handle.model.data[handle.row[0]]}
                ),
            )
        ),
        # Edit fg color with text. TraitError may occur.
        ItemDelegate(
            is_delegate_for=lambda *args: (
                not is_column_header(*args) and is_column_index(4)(*args)
            ),
            validator=validate_is_color_name,
            from_text=lambda _, value: value,
        ),
        # For the Person instance
        ItemDelegate(
            is_delegate_for=lambda *args: (
                not is_column_header(*args) and is_column_index(5)(*args)
            ),
            to_text=lambda _, value: value.name,
            item_editor_factory=TraitsUIItemEditorFactory(
                style="custom",
                editor_factory=InstanceEditor(),
            ),
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
