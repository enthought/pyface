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


class NewRowTableDataModel(RowTableDataModel):
    """ Overridden RowTableDataModel to demonstrate proposed changes.

    The get_value_type is overridden to ensure that AbstractValueType are not
    used.
    """

    def get_value_type(self, row, column):
        raise RuntimeError("Remove value type from model.")

    def get_item_delegate(self, row, column):
        """ Return the ItemDelegate that holds the information about how
        an item is displayed and edited.
        """
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]
        if len(row) == 0:
            return column_data.title_item_delegate
        return column_data.value_item_delegate


class ItemHandle:
    """ This is an object given to delegates and item editors for
    displaying and editing item value.
    """

    def __init__(self, *, model, row, column, delegate):
        self.model = model
        self.row = row
        self.column = column
        self.delegate = delegate

    def set_value(self, value):
        """ Set model value with validation and exception handling.

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

    The factory does not require if the editor value to come from an HasTraits
    object. The flip side of that lack of information is that if the value
    refers to a trait, the TraitType information is not available and some
    TraitsUI editors use the trait type to deduce the default editor.
    That might be an acceptable limitation if it can always be easily overcome.

    For example, when editing a list using ListEditor, one needs to
    define the ListEditor like this:

        ListEditor(trait_handler=List(Str()))

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

        # Hold the value in a separate object to defer committing changes.
        holder_object = TraitsUIItemObject(
            value=item_handle.model.get_value(
                item_handle.row, item_handle.column
            ),
        )

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
            ItemHandle.set_value.
        """
        item_handle.set_value(control._editor.object.value)

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

    """

    # Callable(ItemHandle, value) -> boolean
    # Note that the value has already been transformed back to the business
    # specifiv value as is found on the data model.
    validator = Callable(default_value=lambda _, value: True)

    # Callable(ItemHandle) -> boolean
    # Whether the item is editable. If the callable is unset, then an
    # item is editable if from_text or item_editor_factory is defined.
    # If this is set, then the item is editable only if is_editable returns
    # true and other editors exist. This is useful for dynamically disabling
    # editing capability of an item.
    is_editable = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, any) -> str
    # This converts data model value to text, e.g. for display.
    # This cannot be none.
    to_text = Callable(
        default_value=lambda _, value: str(value), allow_none=False
    )

    # Callable(ItemHandle, str) -> any
    # This converts textual value to a value the data model can understand
    # and set. e.g. this is used when the value is edited as text.
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
    # The default value is None, which means there are no background colors.
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
        delegate = item_model.model.get_item_delegate(row, column)
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

        delegate = self.model.get_item_delegate(row, column)
        item_handle = self._get_handle_for_delegate(row, column, delegate)

        has_editors = any((
                delegate.from_text is not None,
                delegate.item_editor_factory is not None,
        ))

        if delegate.is_editable is None:
            editable = has_editors
        else:
            editable = delegate.is_editable(item_handle) and has_editors

        if editable:
            flags |= Qt.ItemIsEditable

        if delegate.to_check_state is not None:
            flags |= Qt.ItemIsUserCheckable

        return flags

    def data(self, index, role=Qt.DisplayRole):
        """ Reimplemented data to use delegates instead of ValueType."""
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value = self.model.get_value(row, column)

        delegate = self.model.get_item_delegate(row, column)
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

        delegate = self.model.get_item_delegate(row, column)
        item_handle = self._get_handle_for_delegate(row, column, delegate)

        if (delegate.is_editable is not None
                and not delegate.is_editable(item_handle)):
            return False

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

        delegate = self.model.get_item_delegate(row, column)
        item_handle = self._get_handle_for_delegate(row, column, delegate)
        value = self.model.get_value(row, column)
        if role == Qt.DisplayRole and delegate.to_text is not None:
            return delegate.to_text(item_handle, value)
        return None

    # Private methods

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

    def _create_item_model(self):
        self._item_model = NewDataViewItemModel(
            self.data_model,
            self.selection_type,
            self.exporters,
        )


    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        control = super()._create_control(parent)
        control.setItemDelegate(QtCustomItemDelegate(control))
        return control


class NewAttributeDataAccessor(AttributeDataAccessor):
    """ Overridden AttributeDataAccessor to demonstrate passing
    ItemDelegate from NewRowTableDataModel.get_item_delegate.
    """

    # Item delegate for the title (column header)
    # Default is a delegate for displaying the value's text representation.
    # Note that this makes the 'title' trait redundant.
    title_item_delegate = Instance(ItemDelegate, ())

    # Item delegate for the value.
    # Default is a delegate for displaying the value's text representation
    # with no editing allowed.
    value_item_delegate = Instance(ItemDelegate, ())

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
        data_model = create_model()
        widget = NewDataViewWidget(
            parent=parent,
            data_model=data_model,
        )
        widget._create()
        return widget.control


class Person(HasStrictTraits):

    name = Str()

    age = Int()

    # This demonstrates overriding editable state.
    # If false, the range editor for editing age cannot be open.
    is_age_editable = Bool(True)

    favorite_bg_color = Enum(values="bg_color_choices")

    bg_color_choices = List(Str(), ["red", "blue", "black"])

    favorite_fg_color = Enum(values="fg_color_choices")

    fg_color_choices = List(Str(), ["yellow", "grey", "white"])

    greeting = Str("Hello")

    married = Bool()

    # Instance of Person as well.
    child = Any()


def create_model():
    """ Return a DataModel and a list of ItemDelegate for the widget.

    Returns
    -------
    model : AbstractDataModel
    """

    # demonstrate using TraitsUI editor in ItemDelegate
    from traitsui.api import (
        EnumEditor, TextEditor, RangeEditor, InstanceEditor, ListEditor
    )

    names = itertools.cycle(["John", "Mary", "Peter"])
    child_names = itertools.cycle(["Paul", "Joey", "Alex"])
    bg_colors = itertools.cycle(["red", "blue", "black"])
    fg_colors = itertools.cycle(["yellow", "grey", "white"])
    objects = [
        Person(
            name=next(names),
            favorite_bg_color=next(bg_colors),
            favorite_fg_color=next(fg_colors),
            child=Person(name=next(child_names)),
        )
        for _ in range(1000)
    ]

    column_data = [
        NewAttributeDataAccessor(
            attr="age",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "age",
            ),
            # This shows using the RangeEditor as custom editor.
            value_item_delegate=ItemDelegate(
                validator=lambda _, value: value <= 100,
                is_editable=lambda handle: (
                    handle.model.data[handle.row[0]].is_age_editable
                ),
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=RangeEditor(low=0, high=100),
                )
            ),
        ),
        NewAttributeDataAccessor(
            attr="age",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "read only",
            ),
            # default value_item_delegate is a non-editable text.
        ),
        NewAttributeDataAccessor(
            attr="is_age_editable",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "can edit age?",
            ),
            value_item_delegate=ItemDelegate(
                from_text=lambda _, value: (
                    {"true": True, "false": False}[value.lower()]
                ),
                to_check_state=bool_to_check_state,
                from_check_state=check_state_to_bool,
            ),
        ),
        NewAttributeDataAccessor(
            attr="married",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "married",
            ),
            # This shows the checkbox along with editing text to be converted to
            # bool.
            value_item_delegate=ItemDelegate(
                is_editable=lambda handle: (
                    # only editable if the person has come of age.
                    handle.model.data[handle.row[0]].age >= 18
                ),
                to_text=lambda _, value: {True: "Yes", False: "No"}[value],
                to_check_state=bool_to_check_state,
                from_check_state=check_state_to_bool,
            ),
        ),
        NewAttributeDataAccessor(
            attr="favorite_bg_color",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "bg color",
            ),
            # This shows using EnumEditor and having the options dynamically
            # updated.
            value_item_delegate=ItemDelegate(
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
        ),
        NewAttributeDataAccessor(
            attr="bg_color_choices",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "bg color choices",
            ),
            value_item_delegate=ItemDelegate(
                to_text=lambda _, value: next(iter(value), ""),
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=ListEditor(
                        # Otherwise the editor does not know what
                        # item editor to use.
                        trait_handler=List(Str()),
                    ),
                ),
            ),
        ),
        NewAttributeDataAccessor(
            attr="favorite_fg_color",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "fg color",
            ),
            # Edit fg color with text. TraitError may occur but it won't crash
            # the application and the value is not edited in that case.
            value_item_delegate=ItemDelegate(
                validator=validate_is_color_name,
                from_text=lambda _, value: value,
            ),
        ),
        NewAttributeDataAccessor(
            attr="fg_color_choices",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "fg color choices",
            ),
            value_item_delegate=ItemDelegate(
                to_text=lambda _, value: next(iter(value), ""),
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=ListEditor(
                        # Otherwise the editor does not know what
                        # item editor to use.
                        trait_handler=List(Str()),
                    ),
                ),
            ),
        ),
        NewAttributeDataAccessor(
            # This edits the Person instance with the InstanceEditor.
            attr="child",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "child",
            ),
            value_item_delegate=ItemDelegate(
                to_text=lambda _, value: value.name,
                item_editor_factory=TraitsUIItemEditorFactory(
                    style="custom",
                    editor_factory=InstanceEditor(),
                ),
            ),
        ),
    ]

    model = NewRowTableDataModel(
        data=objects,
        row_header_data=NewAttributeDataAccessor(
            attr='greeting',
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_text=lambda _, value: "multi-line text",
            ),
            # This shows using the custom multi-line text editor.
            value_item_delegate=ItemDelegate(
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
        ),
        column_data=column_data,
    )

    return model


def run():
    window = MainWindow()
    window._create()
    window.show(True)
    window.open()
    GUI().start_event_loop()


if __name__ == "__main__":
    run()
