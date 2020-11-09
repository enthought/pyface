""" This module shows changes made to the existing library core objects.
"""

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

from pyface.data_view.poc.custom_editor import (
    BaseItemEditorFactory,
)


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

    def can_set_value(self, row, column):
        raise RuntimeError("I am not needed any more")


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
    # item is editable if from_editable_value or item_editor_factory is defined.
    # If this is set, then the item is editable only if is_editable returns
    # true and other editors exist. This is useful for dynamically disabling
    # editing capability of an item.
    is_editable = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, any) -> str
    # This converts data model value to text, e.g. for display.
    # This cannot be none.
    to_display_text = Callable(
        default_value=lambda _, value: str(value), allow_none=False
    )

    # Callable(ItemHandle, any) -> str
    # This converts data model value to a value that can be edited directly.
    # In Qt, Qt will choose a default widget based on the type
    # of the value returned. e.g. if a string is returned, a single-line text
    # editor will be used. This is also used for the custom editor.
    to_editable_value = Callable(default_value=None, allow_none=True)

    # Callable(ItemHandle, any) -> any
    # This converts the editable value (in the same type as is returned by
    # to_editable_value) back to a value the data model can understand
    # and set. e.g. this can be used when the value is edited as text.
    from_editable_value = Callable(default_value=None, allow_none=True)

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
        if hasattr(editor, "_item_handle"):
            rect = option.rect
            editor_size = editor.sizeHint()

            # This makes sure the editor can be seen, otherwise it
            # takes on the size of the cell, which could be too small.
            if rect.height() < editor_size.height():
                rect.setHeight(editor_size.height())
            if rect.width() < editor_size.width():
                rect.setWidth(editor_size.width())

            editor.setGeometry(rect)
        else:
            super().updateEditorGeometry(editor, option, index)

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
                delegate.from_editable_value is not None,
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

        if role == Qt.DisplayRole and delegate.to_display_text is not None:
            return delegate.to_display_text(item_handle, value)

        if role == Qt.EditRole and delegate.to_editable_value is not None:
            return delegate.to_editable_value(item_handle, value)

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
                and delegate.from_editable_value is not None):
            return self._set_value_with_exception(
                item_handle=item_handle,
                value=value,
                mapper=delegate.from_editable_value,
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
        if role == Qt.DisplayRole and delegate.to_display_text is not None:
            return delegate.to_display_text(item_handle, value)
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
