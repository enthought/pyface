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

from traits.api import Instance, observe, provides

from wx.dataview import (
    DataViewCtrl, DataViewModel as wxDataViewModel, DATAVIEW_CELL_EDITABLE,
    DATAVIEW_CELL_ACTIVATABLE
)
from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget
)
from pyface.data_view.data_view_errors import DataViewGetError
from pyface.ui.wx.widget import Widget
from .data_view_model import DataViewModel


logger = logging.getLogger(__name__)


# XXX This file is scaffolding and may need to be rewritten

@provides(IDataViewWidget)
class DataViewWidget(MDataViewWidget, Widget):
    """ The Wx implementation of the DataViewWidget. """

    #: The QAbstractItemModel instance used by the view.  This will
    #: usually be a DataViewModel subclass.
    _item_model = Instance(wxDataViewModel)

    def _create_control(self, parent):
        """ Create the DataViewWidget's toolkit control. """
        self._create_item_model()

        control = DataViewCtrl(parent)
        control.AssociateModel(self._item_model)
        # required for wxPython refcounting system
        self._item_model.DecRef()

        # create columns for view
        value_type = self._item_model.model.get_value_type([], [])
        try:
            text = value_type.get_text(self._item_model.model, [], [])
        except DataViewGetError:
            text = ''
        except Exception:
            # unexpected error, log and raise
            logger.exception("get header data failed: column ()")
            raise
        control.AppendTextColumn(text, 0, mode=DATAVIEW_CELL_ACTIVATABLE)

        for column in range(self._item_model.GetColumnCount()-1):
            value_type = self._item_model.model.get_value_type([], [column])
            try:
                text = value_type.get_text(self._item_model.model, [], [column])
            except DataViewGetError:
                text = ''
            except Exception:
                # unexpected error, log and raise
                logger.exception(
                    "get header data failed: column (%r,)",
                    column,
                )
                raise

            control.AppendTextColumn(
                text,
                column+1,
                mode=DATAVIEW_CELL_EDITABLE,
            )
        return control

    def _create_item_model(self):
        """ Create the DataViewItemModel which wraps the data model. """
        self._item_model = DataViewModel(self.data_model)

    def destroy(self):
        """ Perform any actions required to destroy the control. """
        super().destroy()
        # ensure that we release the reference to the item model
        self._item_model = None

    def _get_control_header_visible(self):
        """ Method to get the control's header visibility. """
        # TODO: need to read DV_NO_HEADER
        pass

    def _set_control_header_visible(self, tooltip):
        """ Method to set the control's header visibility. """
        # TODO: need to toggle DV_NO_HEADER
        pass

    @observe('data_model', dispatch='ui')
    def update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new
