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

from traits.api import Callable, Enum, Instance, observe, provides

from pyface.qt.QtCore import (
    QAbstractItemModel, QItemSelection, QItemSelectionModel
)
from pyface.qt.QtGui import QAbstractItemView, QTreeView
from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget
)
from pyface.ui.qt.layout_widget import LayoutWidget
from .data_view_item_model import DataViewItemModel

# XXX This file is scaffolding and may need to be rewritten

logger = logging.getLogger(__name__)

qt_selection_types = {
    "row": QAbstractItemView.SelectionBehavior.SelectRows,
    "column": QAbstractItemView.SelectionBehavior.SelectColumns,
    "item": QAbstractItemView.SelectionBehavior.SelectItems,
}
pyface_selection_types = {
    value: key for key, value in qt_selection_types.items()
}
qt_selection_modes = {
    "none": QAbstractItemView.SelectionMode.NoSelection,
    "single": QAbstractItemView.SelectionMode.SingleSelection,
    "extended": QAbstractItemView.SelectionMode.ExtendedSelection,
}
pyface_selection_modes = {
    value: key for key, value in qt_selection_modes.items()
}


class DataViewTreeView(QTreeView):
    """ QTreeView subclass that handles drag and drop via DropHandlers. """

    _widget = None

    def dragEnterEvent(self, event):
        drop_handler = self._get_drop_handler(event)
        if drop_handler is not None:
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        drop_handler = self._get_drop_handler(event)
        if drop_handler is not None:
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dragLeaveEvent(self, event):
        drop_handler = self._get_drop_handler(event)
        if drop_handler is not None:
            event.acceptProposedAction()
        else:
            super().dragLeaveEvent(event)

    def dropEvent(self, event):
        drop_handler = self._get_drop_handler(event)
        if drop_handler is not None:
            drop_handler.handle_drop(event, self)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def _get_drop_handler(self, event):
        if self._widget is not None:
            widget = self._widget
            for drop_handler in widget.drop_handlers:
                if drop_handler.can_handle_drop(event, self):
                    return drop_handler
        return None


@provides(IDataViewWidget)
class DataViewWidget(MDataViewWidget, LayoutWidget):
    """ The Qt implementation of the DataViewWidget. """

    #: Factory for the underlying Qt control, to facilitate replacement
    control_factory = Callable(DataViewTreeView)

    # IDataViewWidget Interface traits --------------------------------------

    #: What can be selected.  Qt supports additional selection types.
    selection_type = Enum("row", "column", "item")

    #: How selections are modified.  Qt supports turning off selections.
    selection_mode = Enum("extended", "none", "single")

    # IWidget Interface traits ----------------------------------------------

    control = Instance(QAbstractItemView)

    # Private traits --------------------------------------------------------

    #: The QAbstractItemModel instance used by the view.  This will
    #: usually be a DataViewItemModel subclass.
    _item_model = Instance(QAbstractItemModel)

    # ------------------------------------------------------------------------
    # IDataViewWidget Interface
    # ------------------------------------------------------------------------

    def _create_item_model(self):
        """ Create the DataViewItemModel which wraps the data model. """
        self._item_model = DataViewItemModel(
            self.data_model,
            self.selection_type,
            self.exporters,
        )

    def _get_control_header_visible(self):
        """ Method to get the control's header visibility. """
        return not self.control.isHeaderHidden()

    def _set_control_header_visible(self, header_visible):
        """ Method to set the control's header visibility. """
        self.control.setHeaderHidden(not header_visible)

    def _get_control_selection_type(self):
        """ Toolkit specific method to get the selection type. """
        qt_selection_type = self.control.selectionBehavior()
        return pyface_selection_types[qt_selection_type]

    def _set_control_selection_type(self, selection_type):
        """ Toolkit specific method to change the selection type. """
        qt_selection_type = qt_selection_types[selection_type]
        self.control.setSelectionBehavior(qt_selection_type)
        self._item_model.selectionType = selection_type

    def _get_control_selection_mode(self):
        """ Toolkit specific method to get the selection mode. """
        qt_selection_mode = self.control.selectionMode()
        return pyface_selection_modes[qt_selection_mode]

    def _set_control_selection_mode(self, selection_mode):
        """ Toolkit specific method to change the selection mode. """
        qt_selection_mode = qt_selection_modes[selection_mode]
        self.control.setSelectionMode(qt_selection_mode)

    def _get_control_selection(self):
        """ Toolkit specific method to get the selection. """
        indices = self.control.selectedIndexes()
        if self.selection_type == 'row':
            return self._item_model._extract_rows(indices)
        elif self.selection_type == 'column':
            return self._item_model._extract_columns(indices)
        else:
            return self._item_model._extract_indices(indices)

    def _set_control_selection(self, selection):
        """ Toolkit specific method to change the selection. """
        selection_model = self.control.selectionModel()
        select_flags = QItemSelectionModel.SelectionFlag.Select
        qt_selection = QItemSelection()

        if self.selection_type == 'row':
            select_flags |= QItemSelectionModel.SelectionFlag.Rows
            for row, column in selection:
                index = self._item_model._to_model_index(row, (0,))
                qt_selection.select(index, index)
        elif self.selection_type == 'column':
            select_flags |= QItemSelectionModel.SelectionFlag.Columns
            for row, column in selection:
                index = self._item_model._to_model_index(
                    row + (0,), column)
                qt_selection.select(index, index)
        else:
            for row, column in selection:
                index = self._item_model._to_model_index(row, column)
                qt_selection.select(index, index)
        selection_model.clearSelection()
        selection_model.select(qt_selection, select_flags)

    def _observe_control_selection(self, remove=False):
        selection_model = self.control.selectionModel()
        if remove:
            try:
                selection_model.selectionChanged.disconnect(
                    self._update_selection
                )
            except (TypeError, RuntimeError):
                # has already been disconnected
                logger.info("selectionChanged already disconnected")
        else:
            selection_model.selectionChanged.connect(self._update_selection)

    # ------------------------------------------------------------------------
    # IWidget Interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        self._create_item_model()

        control = self.control_factory(parent)
        control._widget = self
        control.setUniformRowHeights(True)
        control.setAnimated(True)
        control.setDragEnabled(True)
        control.setModel(self._item_model)
        control.setAcceptDrops(True)
        control.setDropIndicatorShown(True)
        return control

    def destroy(self):
        """ Perform any actions required to destroy the control.
        """
        if self.control is not None:
            self.control.setModel(None)

            # ensure that we release references
            self.control._widget = None
            self._item_model = None

        super().destroy()

    # ------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------

    # Trait observers

    @observe('data_model', dispatch='ui')
    def _update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new

    @observe('exporters.items', dispatch='ui')
    def _update_exporters(self, event):
        if self._item_model is not None:
            self._item_model.exporters = self.exporters
