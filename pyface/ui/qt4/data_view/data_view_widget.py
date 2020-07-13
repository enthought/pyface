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

from traits.api import Bool, Instance, observe, provides

from pyface.qt.QtCore import QAbstractItemModel
from pyface.qt.QtGui import (
    QAbstractItemView, QItemSelection, QItemSelectionModel, QTreeView
)
from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget
)
from pyface.ui.qt4.widget import Widget
from .data_view_item_model import DataViewItemModel

# XXX This file is scaffolding and may need to be rewritten

logger = logging.getLogger(__name__)

qt_selection_types = {
    "row": QAbstractItemView.SelectRows,
    "column": QAbstractItemView.SelectColumns,
    "item": QAbstractItemView.SelectItems,
}
pyface_selection_types = {
    value: key for key, value in qt_selection_types.items()
}
qt_selection_modes = {
    "none": QAbstractItemView.NoSelection,
    "single": QAbstractItemView.SingleSelection,
    "extended": QAbstractItemView.ExtendedSelection,
}
pyface_selection_modes = {
    value: key for key, value in qt_selection_modes.items()
}


@provides(IDataViewWidget)
class DataViewWidget(MDataViewWidget, Widget):
    """ The Qt implementation of the DataViewWidget. """

    control = Instance(QAbstractItemView)

    #: The QAbstractItemModel instance used by the view.  This will
    #: usually be a DataViewItemModel subclass.
    _item_model = Instance(QAbstractItemModel)

    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        self._create_item_model()

        control = QTreeView(parent)
        control.setUniformRowHeights(True)
        control.setAnimated(True)
        control.setModel(self._item_model)
        return control

    def _create_item_model(self):
        """ Create the DataViewItemModel which wraps the data model. """
        self._item_model = DataViewItemModel(self.data_model)

    def destroy(self):
        """ Perform any actions required to destroy the control.
        """
        self.control.setModel(None)
        super().destroy()
        # ensure that we release the reference to the item model
        self._item_model = None

    def _get_control_header_visible(self):
        """ Method to get the control's header visibility. """
        return not self.control.isHeaderHidden()

    def _set_control_header_visible(self, header_visible):
        """ Method to set the control's header visibility. """
        self.control.setHeaderHidden(not header_visible)

    def _get_selection_type(self):
        """ Toolkit specific method to get the selection type. """
        qt_selection_type = self.control.selectionBehavior()
        return pyface_selection_types[qt_selection_type]

    def _set_selection_type(self, selection_type):
        """ Toolkit specific method to change the selection type. """
        qt_selection_type = qt_selection_types[selection_type]
        self.control.setSelectionBehavior(qt_selection_type)

    def _get_selection_mode(self):
        """ Toolkit specific method to get the selection mode. """
        qt_selection_mode = self.control.selectionMode()
        return pyface_selection_modes[qt_selection_mode]

    def _set_selection_mode(self, selection_mode):
        """ Toolkit specific method to change the selection mode. """
        qt_selection_mode = qt_selection_modes[selection_mode]
        self.control.setSelectionMode(qt_selection_mode)

    def _get_selection(self):
        """ Toolkit specific method to get the selection. """
        if self.selection_type == 'item':
            selection = [
                (
                    self._item_model._to_row_index(index),
                    self._item_model._to_column_index(index),
                )
                for index in self.control.selectedIndexes()
            ]
        elif self.selection_type == 'row':
            selection = []
            for index in self.control.selectedIndexes():
                row = self._item_model._to_row_index(index)
                if (row, ()) not in selection:
                    selection.append((row, ()))
        elif self.selection_type == 'column':
            selection = []
            for index in self.control.selectedIndexes():
                row = self._item_model._to_row_index(index)[:-1]
                column = self._item_model._to_column_index(index)
                if (row, column) not in selection:
                    selection.append((row, column))
        else:
            selection = []
        return selection

    def _set_selection(self, selection):
        """ Toolkit specific method to change the selection. """
        if self.selection_mode == 'none':
            selection = []
        elif self.selection_mode == 'single':
            selection = selection[-1:]

        selection_model = self.control.selectionModel()
        select_flags = QItemSelectionModel.Select
        qt_selection = QItemSelection()

        if self.selection_type == 'item':
            for row, column in selection:
                index = self._item_model._to_model_index(row, column)
                qt_selection.select(index, index)
        elif self.selection_type == 'row':
            select_flags |= QItemSelectionModel.Rows
            for row, column in selection:
                index = self._item_model._to_model_index(row, (0,))
                qt_selection.select(index, index)
        elif self.selection_type == 'column':
            select_flags |= QItemSelectionModel.Columns
            for row, column in selection:
                index = self._item_model._to_model_index(
                    row + (0,), column)
                qt_selection.select(index, index)
        selection_model.clearSelection()
        selection_model.select(qt_selection, select_flags)

    def _observe_selection(self, remove=False):
        selection_model = self.control.selectionModel()
        if remove:
            try:
                selection_model.selectionChanged.disconnect(
                  self._update_selection
                )
            except TypeError:
                # has already been disconnected
                logger.info("selectionChanged already disconnected")
        else:
            selection_model.selectionChanged.connect(self._update_selection)

    def _update_selection(self, selected, deselected):
        with self._selection_updating():
            self.selection = self._get_selection()

    @observe('data_model', dispatch='ui')
    def update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new
