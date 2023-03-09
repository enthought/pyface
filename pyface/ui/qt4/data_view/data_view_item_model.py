# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging

from pyface.qt import is_qt4
from pyface.qt.QtCore import QAbstractItemModel, QMimeData, QModelIndex, Qt
from pyface.qt.QtGui import QColor
from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.abstract_value_type import CheckState
from pyface.data_view.data_view_errors import (
    DataViewGetError, DataViewSetError
)
from pyface.data_view.index_manager import Root
from .data_wrapper import DataWrapper


logger = logging.getLogger(__name__)

# XXX This file is scaffolding and may need to be rewritten

WHITE = QColor(255, 255, 255)
BLACK = QColor(0, 0, 0)

set_check_state_map = {
    Qt.CheckState.Checked: CheckState.CHECKED,
    Qt.CheckState.Unchecked: CheckState.UNCHECKED,
}
get_check_state_map = {
    CheckState.CHECKED: Qt.CheckState.Checked,
    CheckState.UNCHECKED: Qt.CheckState.Unchecked,
}


class DataViewItemModel(QAbstractItemModel):
    """ A QAbstractItemModel that understands AbstractDataModels. """

    def __init__(self, model, selection_type, exporters, parent=None):
        super().__init__(parent)
        self.model = model
        self.selectionType = selection_type
        self.exporters = exporters
        self.destroyed.connect(self._on_destroyed)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: AbstractDataModel):
        self._disconnect_model_observers()
        if hasattr(self, '_model'):
            self.beginResetModel()
            self._model = model
            self.endResetModel()
        else:
            # model is being initialized
            self._model = model
        self._connect_model_observers()

    # model event listeners

    def on_structure_changed(self, event):
        self.beginResetModel()
        self.endResetModel()

    def on_values_changed(self, event):
        top, left, bottom, right = event.new
        if top == () and bottom == ():
            # this is a column header change
            self.headerDataChanged.emit(Qt.Orientation.Horizontal, left[0], right[0])
        elif left == () and right == ():
            # this is a row header change
            # XXX this is currently not supported and not needed
            pass
        else:
            for i, (top_row, bottom_row) in enumerate(zip(top, bottom)):
                if top_row != bottom_row:
                    break
            top = top[:i+1]
            bottom = bottom[:i+1]

            top_left = self._to_model_index(top, left)
            bottom_right = self._to_model_index(bottom, right)
            self.dataChanged.emit(top_left, bottom_right)

    # Structure methods

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        parent = index.internalPointer()
        if parent == Root:
            return QModelIndex()

        grandparent, row = self.model.index_manager.get_parent_and_row(parent)
        return self.createIndex(row, 0, grandparent)

    def index(self, row, column, parent):
        if parent.isValid():
            parent_index = self.model.index_manager.create_index(
                parent.internalPointer(),
                parent.row(),
            )
        else:
            parent_index = Root
        index = self.createIndex(row, column, parent_index)
        return index

    def rowCount(self, index=QModelIndex()):
        row_index = self._to_row_index(index)
        try:
            if self.model.can_have_children(row_index):
                return self.model.get_row_count(row_index)
        except Exception:
            logger.exception("Error in rowCount")

        return 0

    def columnCount(self, index=QModelIndex()):
        row_index = self._to_row_index(index)
        try:
            # the number of columns is constant; leaf rows return 0
            if self.model.can_have_children(row_index):
                return self.model.get_column_count() + 1
        except Exception:
            logger.exception("Error in columnCount")

        return 0

    # Data methods

    def flags(self, index):
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value_type = self.model.get_value_type(row, column)
        if row == () and column == ():
            return Qt.ItemFlag.ItemIsEnabled

        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled
        if not is_qt4 and not self.model.can_have_children(row):
            flags |= Qt.ItemFlag.ItemNeverHasChildren

        try:
            if value_type:
                if value_type.has_editor_value(self.model, row, column):
                    flags |= Qt.ItemFlag.ItemIsEditable
                if (
                    value_type.has_check_state(self.model, row, column)
                    and self.model.can_set_value(row, column)
                ):
                    flags |= Qt.ItemFlag.ItemIsUserCheckable
        except DataViewGetError:
            # expected error, ignore
            pass
        except Exception:
            # unexpected error, log and raise
            logger.exception(
                "get flags failed: row %r, column %r",
                row,
                column,
            )
            raise

        return flags

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value_type = self.model.get_value_type(row, column)
        try:
            if not value_type:
                return None

            if role == Qt.ItemDataRole.DisplayRole:
                if value_type.has_text(self.model, row, column):
                    return value_type.get_text(self.model, row, column)
            elif role == Qt.ItemDataRole.EditRole:
                if value_type.has_editor_value(self.model, row, column):
                    return value_type.get_editor_value(self.model, row, column)
            elif role == Qt.ItemDataRole.DecorationRole:
                if value_type.has_image(self.model, row, column):
                    image = value_type.get_image(self.model, row, column)
                    if image is not None:
                        return image.create_image()
            elif role == Qt.ItemDataRole.BackgroundRole:
                if value_type.has_color(self.model, row, column):
                    color = value_type.get_color(self.model, row, column)
                    if color is not None:
                        return color.to_toolkit()
            elif role == Qt.ItemDataRole.ForegroundRole:
                if value_type.has_color(self.model, row, column):
                    color = value_type.get_color(self.model, row, column)
                    if color is not None and color.is_dark:
                        return WHITE
                    else:
                        return BLACK
            elif role == Qt.ItemDataRole.CheckStateRole:
                if value_type.has_check_state(self.model, row, column):
                    value = value_type.get_check_state(self.model, row, column)
                    return get_check_state_map[value]
            elif role == Qt.ItemDataRole.ToolTipRole:
                if value_type.has_tooltip(self.model, row, column):
                    return value_type.get_tooltip(self.model, row, column)
        except DataViewGetError:
            # expected error, ignore
            pass
        except Exception:
            # unexpected error, log and raise
            logger.exception(
                "get data failed: row %r, column %r",
                row,
                column,
            )
            raise

        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value_type = self.model.get_value_type(row, column)
        if not value_type:
            return False

        try:
            if role == Qt.ItemDataRole.EditRole:
                if value_type.has_editor_value(self.model, row, column):
                    value_type.set_editor_value(self.model, row, column, value)
            elif role == Qt.ItemDataRole.DisplayRole:
                if value_type.has_text(self.model, row, column):
                    value_type.set_text(self.model, row, column, value)
            elif role == Qt.ItemDataRole.CheckStateRole:
                if value_type.has_check_state(self.model, row, column):
                    state = set_check_state_map[Qt.CheckState(value)]
                    value_type.set_check_state(self.model, row, column, state)

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

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            row = ()
            if section == 0:
                column = ()
            else:
                column = (section - 1,)
        else:
            # XXX not currently used, but here for symmetry and completeness
            row = (section,)
            column = ()

        value_type = self.model.get_value_type(row, column)

        try:
            if role == Qt.ItemDataRole.DisplayRole:
                if value_type.has_text(self.model, row, column):
                    return value_type.get_text(self.model, row, column)
        except DataViewGetError:
            # expected error, ignore
            pass
        except Exception:
            # unexpected error, log and raise
            logger.exception(
                "get header data failed: row %r, column %r",
                row,
                column,
            )
            raise

        return None

    def mimeData(self, indexes):
        mimedata = super().mimeData(indexes)
        if mimedata is None:
            mimedata = QMimeData()
        data_wrapper = DataWrapper(toolkit_data=mimedata)

        indices = self._normalize_indices(indexes)
        for exporter in self.exporters:
            try:
                exporter.add_data(data_wrapper, self.model, indices)
            except Exception:
                # unexpected error, log and raise
                logger.exception(
                    "data export failed: mimetype {}, indices {}",
                    exporter.format.mimetype,
                    indices,
                )
                raise

        return data_wrapper.toolkit_data

    # Private utility methods

    def _on_destroyed(self):
        self._disconnect_model_observers()
        self._model = None

    def _connect_model_observers(self):
        if getattr(self, "_model", None) is not None:
            self._model.observe(
                self.on_structure_changed,
                'structure_changed',
                dispatch='ui',
            )
            self._model.observe(
                self.on_values_changed,
                'values_changed',
                dispatch='ui',
            )

    def _disconnect_model_observers(self):
        if getattr(self, "_model", None) is not None:
            self._model.observe(
                self.on_structure_changed,
                'structure_changed',
                dispatch='ui',
                remove=True,
            )
            self._model.observe(
                self.on_values_changed,
                'values_changed',
                dispatch='ui',
                remove=True,
            )

    def _to_row_index(self, index):
        if not index.isValid():
            row_index = ()
        else:
            parent = index.internalPointer()
            if parent == Root:
                row_index = ()
            else:
                row_index = self.model.index_manager.to_sequence(parent)
            row_index += (index.row(),)
        return row_index

    def _to_column_index(self, index):
        if not index.isValid():
            return ()
        else:
            column = index.column()
            if column == 0:
                return ()
            else:
                return (column - 1,)

    def _to_model_index(self, row_index, column_index):
        if len(row_index) == 0:
            return QModelIndex()
        index = self.model.index_manager.from_sequence(row_index[:-1])
        row = row_index[-1]
        if len(column_index) == 0:
            column = 0
        else:
            column = column_index[0] + 1

        return self.createIndex(row, column, index)

    def _extract_rows(self, indices):
        rows = []
        for index in indices:
            row = self._to_row_index(index)
            if (row, ()) not in rows:
                rows.append((row, ()))
        return rows

    def _extract_columns(self, indices):
        columns = []
        for index in indices:
            row = self._to_row_index(index)[:-1]
            column = self._to_column_index(index)
            if (row, column) not in columns:
                columns.append((row, column))
        return columns

    def _extract_indices(self, indices):
        return [
            (self._to_row_index(index), self._to_column_index(index))
            for index in indices
        ]

    def _normalize_indices(self, indices):
        if self.selectionType == 'row':
            return self._extract_rows(indices)
        elif self.selectionType == 'column':
            return self._extract_columns(indices)
        else:
            return self._extract_indices(indices)
