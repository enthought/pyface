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

from wx.dataview import (
    DataViewCtrl, DataViewModel as wxDataViewModel, DATAVIEW_CELL_EDITABLE
)
from pyface.data_view.abstract_data_model import AbstractDataModel
from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget
)
from pyface.ui.wx.widget import Widget
from .data_view_model import DataViewModel


# XXX This file is scaffolding and may need to be rewritten

@provides(IDataViewWidget)
class DataViewWidget(MDataViewWidget, Widget):

    _item_model = Instance(wxDataViewModel)

    def _create_control(self, parent):
        self._create_item_model()

        control = DataViewCtrl(parent)
        control.AssociateModel(self._item_model)
        # required for wxPython refcounting system
        self._item_model.DecRef()

        # create columns for view
        for column in range(self._item_model.GetColumnCount()):
            control.AppendTextColumn(
                self._item_model.model.get_text([], [column]),
                column,
                mode=DATAVIEW_CELL_EDITABLE,
            )
        return control

    def _create_item_model(self):
        self._item_model = DataViewModel(self.data_model)

    def _get_control_header_visible(self):
        """ Toolkit specific method to get the control's tooltip. """
        #return not self.control.isHeaderHidden()

    def _set_control_header_visible(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        #self.control.setHeaderHidden(not tooltip)

    @observe('data_model', dispatch='ui')
    def update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new



