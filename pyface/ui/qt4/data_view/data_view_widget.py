# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Bool, Instance, observe, provides

from pyface.qt.QtCore import QAbstractItemModel
from pyface.qt.QtGui import QTreeView
from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget
)
from pyface.ui.qt4.widget import Widget
from .data_view_item_model import DataViewItemModel

# XXX This file is scaffolding and may need to be rewritten


@provides(IDataViewWidget)
class DataViewWidget(MDataViewWidget, Widget):
    """ The Qt implementation of the DataViewWidget. """

    #: The QAbstractItemModel instance used by the view.  This will
    #: usually be a DataViewItemModel subclass.
    _item_model = Instance(QAbstractItemModel)

    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        self._create_item_model()

        control = QTreeView(parent)
        control.setUniformRowHeights(True)
        control.setModel(self._item_model)
        control.setHeaderHidden(not self.header_visible)
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

    def _set_control_header_visible(self, tooltip):
        """ Method to set the control's header visibility. """
        self.control.setHeaderHidden(not tooltip)

    @observe('data_model', dispatch='ui')
    def update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new
