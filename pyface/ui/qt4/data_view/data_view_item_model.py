# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging

from pyface.qt.QtCore import QAbstractItemModel, QModelIndex, Qt
from pyface.data_view.index_manager import Root
from pyface.data_view.abstract_data_model import AbstractDataModel


logger = logging.getLogger(__name__)

# XXX This file is scaffolding and may need to be rewritten


class DataViewItemModel(QAbstractItemModel):

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.showRowHeader = True

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model: AbstractDataModel):
        if hasattr(self, '_model'):
            # disconnect trait listeners
            self._model.observe(
                self.on_structure_changed,
                'structure_changed',
                remove=True,
            )
            self._model.observe(
                self.on_values_changed,
                'values_changed',
                remove=True,
            )

            self.beginResetModel()
            self._model = model
            self.endResetModel()
        else:
            # model is being initialized
            self._model = model

        # hook up trait listeners
        self._model.observe(
            self.on_structure_changed,
            'structure_changed',
        )
        self._model.observe(
            self.on_values_changed,
            'values_changed',
        )

    # model event listeners

    def on_structure_changed(self, event):
        self.beginResetModel()
        self.endResetModel()

    def on_values_changed(self, event):
        top, left, bottom, right = event.new
        if top == [] and bottom == []:
            # this is a column header change
            self.headerDataChanged.emit(left[0], right[0])
        elif left == [] and right == []:
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

    def rowCount(self, index):
        row_index = self._to_row_index(index)
        try:
            if self.model.can_have_children(row_index):
                return self.model.get_row_count(row_index)
        except Exception:
            logger.exception("Error in rowCount")

        return 0

    def columnCount(self, index):
        row_index = self._to_row_index(index)
        try:
            return self.model.get_column_count(row_index) + 1
        except Exception:
            logger.exception("Error in columnCount")

    # Data methods

    def flags(self, index):
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value_type = self.model.get_value_type(row, column)

        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if not self.model.can_have_children(row):
            flags |= Qt.ItemNeverHasChildren

        if value_type.get_is_editable(self.model, row, column):
            flags |= Qt.ItemIsEditable

        return flags

    def data(self, index, role=Qt.DisplayRole):
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value_type = self.model.get_value_type(row, column)

        if role == Qt.DisplayRole:
            if value_type.has_text(self.model, row, column):
                return value_type.get_text(self.model, row, column)
        elif role == Qt.EditRole:
            if value_type.get_is_editable(self.model, row, column):
                return value_type.get_editable(self.model, row, column)

        return None

    def setData(self, index, value, role=Qt.EditRole):
        row = self._to_row_index(index)
        column = self._to_column_index(index)
        value_type = self.model.get_value_type(row, column)

        if role == Qt.EditRole:
            if value_type.get_is_editable(self.model, row, column):
                return value_type.set_editable(self.model, row, column, value)
        elif role == Qt.TextRole:
            if value_type.has_text(self.model, row, column):
                return value_type.set_text(self.model, row, column, value)

        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            row = []
            if section == 0:
                column = []
            else:
                column = [section - 1]
        else:
            # XXX not currently used, but here for symmetry and completeness
            row = [section]
            column = []

        value_type = self.model.get_value_type(row, column)

        if role == Qt.DisplayRole:
            if value_type.has_text(self.model, row, column):
                return value_type.get_text(self.model, row, column)

    # Private utility methods

    def _to_row_index(self, index):
        if not index.isValid():
            row_index = []
        else:
            parent = index.internalPointer()
            if parent == Root:
                row_index = []
            else:
                row_index = self.model.index_manager.to_sequence(parent)
            row_index.append(index.row())
        return row_index

    def _to_column_index(self, index):
        if not index.isValid():
            return []
        else:
            column = index.column()
            if column == 0:
                return []
            else:
                return [column - 1]

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

