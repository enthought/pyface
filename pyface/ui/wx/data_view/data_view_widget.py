# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, observe, provides

from wx.dataview import (
    DataViewCtrl, DataViewModel as wxDataViewModel, DATAVIEW_CELL_EDITABLE,
    DATAVIEW_CELL_ACTIVATABLE
)
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
        value_type = self._item_model.model.get_value_type([], [])
        control.AppendTextColumn(
            value_type.get_text(self._item_model.model, [], []),
            0,
            mode=DATAVIEW_CELL_ACTIVATABLE,
        )
        for column in range(self._item_model.GetColumnCount()-1):
            value_type = self._item_model.model.get_value_type([], [column])
            control.AppendTextColumn(
                value_type.get_text(self._item_model.model, [], [column]),
                column+1,
                mode=DATAVIEW_CELL_EDITABLE,
            )
        return control

    def _create_item_model(self):
        self._item_model = DataViewModel(self.data_model)

    def destroy(self):
        if self.control is not None:
            # unhook things here
            self._item_model = None
        super().destroy()

    def _get_control_header_visible(self):
        """ Toolkit specific method to get the control's tooltip. """
        # need to read DV_NO_HEADER
        pass

    def _set_control_header_visible(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        # need to toggle DV_NO_HEADER
        pass

    @observe('data_model', dispatch='ui')
    def update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new
