""" This module extends the existing library with the proposed
custom editor features, using an approach that follows more or less
what Corran has proposed.

There are some elements of guessing here of what Corran meant.
"""

from traits.api import List

# Use Qt implementations for proof-of-concept purposes.
from pyface.qt import is_qt5
from pyface.qt.QtCore import Qt
from pyface.qt.QtGui import (
    QStyledItemDelegate,
)
from pyface.ui.qt4.data_view.data_view_widget import DataViewWidget


class ItemHandle:
    """ This object represents an item at a specific row and column
    in a given data model.

    Parameters
    ----------
    model : AbstractDataModel
    row : tuple of int
    column : tuple of int
    """

    def __init__(self, *, model, row, column):
        self.model = model
        self.row = row
        self.column = column

    def set_value(self, value):
        """ Set model value with exception handling.

        Parameters
        ----------
        value : any
            Value to be set on the Model.
        """
        # Contrast: No validation here.

        try:
            self.model.set_value(
                self.row, self.column, value
            )
        except DataViewSetError:
            pass


class QtCustomItemDelegate(QStyledItemDelegate):
    """ Custom implementation of the QAbstractItemDelegate to support
    custom editor.
    """

    def __init__(self, parent, data_view_widget):
        """ Overridden so the item delegate holds a reference back to
        the data view widget.

        This creates a cycle reference... data view widget holds a reference
        to the QAbstractItemView, which holds a reference to this
        QStyledItemDelegate, which holds a reference back to the
        data view widget.

        This cycle reference is not needed in the other design.
        """
        super().__init__(parent)
        self._data_view_widget = data_view_widget

    def createEditor(self, parent, option, index):
        """ Reimplemented to return the editor for a given index."""

        item_model = index.model()
        row = item_model._to_row_index(index)
        column = item_model._to_column_index(index)

        try:
            delegate = self._data_view_widget._get_item_delegate(
                item_model.model, row, column
            )
        except RuntimeError:
            return super().createEditor(parent, option, index)

        if delegate.item_editor_factory is not None:
            item_handle = ItemHandle(
                model=item_model.model,
                row=row,
                column=column,
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
        This method is the same as the one in 'modified_lib.py'

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
        """
        This method is the same as the one in 'modified_lib.py'

        Update the editor's geometry.
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
            """
            This method is the same as the one in 'modified_lib.py'

            Override behaviour to do with destroying the editor
            """
            if hasattr(editor, "_item_editor_factory"):
                try:
                    editor._item_editor_factory.destroy(editor)
                except NotImplementedError:
                    super().destroyEditor(editor, index)
            else:
                # this simply calls editor.deleteLater
                super().destroyEditor(editor, index)


class NewDataViewWidget(DataViewWidget):
    """ Extend DataViewWidget to support the proposed custom editor
    feature.
    """

    item_delegates = List()

    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        control = super()._create_control(parent)

        # Smell: Otherwise there are no ways for the Qt item delegate
        # to find the pyface item delegate defined on this DataViewWidget.
        # This is a pattern also seen in TraitsUI table editor.

        control.setItemDelegate(
            QtCustomItemDelegate(control, self)
        )

        return control

    def _get_item_delegate(self, model, row, column):
        """ This is the contentious part... how do we get the custom
        editor for a given row and column.
        """
        for item_delegate in self.item_delegates:
            if item_delegate.is_delegate_for(model, row, column):
                return item_delegate
        raise RuntimeError("No custom item delegates are available.")
