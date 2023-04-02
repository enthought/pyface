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
import warnings

import wx
from wx.dataview import (
    DataViewCtrl, DataViewEvent, DataViewItemArray,
    DataViewModel as wxDataViewModel,
    DATAVIEW_CELL_EDITABLE, DATAVIEW_CELL_ACTIVATABLE,
    DV_MULTIPLE, DV_NO_HEADER, EVT_DATAVIEW_SELECTION_CHANGED,
    wxEVT_DATAVIEW_SELECTION_CHANGED
)

from traits.api import Enum, Instance, observe, provides

from pyface.data_view.i_data_view_widget import (
    IDataViewWidget, MDataViewWidget
)
from pyface.data_view.data_view_errors import DataViewGetError
from pyface.ui.wx.layout_widget import LayoutWidget
from .data_view_model import DataViewModel


logger = logging.getLogger(__name__)


# XXX This file is scaffolding and may need to be rewritten

@provides(IDataViewWidget)
class DataViewWidget(MDataViewWidget, LayoutWidget):
    """ The Wx implementation of the DataViewWidget. """

    #: What can be selected.
    selection_type = Enum("row")

    #: How selections are modified.
    selection_mode = Enum("extended", "single")

    # Private traits --------------------------------------------------------

    #: The QAbstractItemModel instance used by the view.  This will
    #: usually be a DataViewModel subclass.
    _item_model = Instance(wxDataViewModel)

    # ------------------------------------------------------------------------
    # IDataViewWidget Interface
    # ------------------------------------------------------------------------

    def _create_item_model(self):
        """ Create the DataViewItemModel which wraps the data model. """
        self._item_model = DataViewModel(self.data_model)

    def _get_control_header_visible(self):
        """ Method to get the control's header visibility. """
        return not self.control.GetWindowStyleFlag() & DV_NO_HEADER

    def _set_control_header_visible(self, header_visible):
        """ Method to set the control's header visibility. """
        old_visible = self._get_control_header_visible()
        if header_visible != old_visible:
            self.control.ToggleWindowStyle(DV_NO_HEADER)

    def _get_control_selection_type(self):
        """ Toolkit specific method to get the selection type. """
        return "row"

    def _set_control_selection_type(self, selection_type):
        """ Toolkit specific method to change the selection type. """
        if selection_type != "row":
            warnings.warn(
                "{!r} selection_type not supported in Wx".format(
                    selection_type
                ),
                RuntimeWarning,
            )

    def _get_control_selection_mode(self):
        """ Toolkit specific method to get the selection mode. """
        if self.control.GetWindowStyleFlag() & DV_MULTIPLE:
            return "extended"
        else:
            return "single"

    def _set_control_selection_mode(self, selection_mode):
        """ Toolkit specific method to change the selection mode. """
        if selection_mode not in {'extended', 'single'}:
            warnings.warn(
                "{!r} selection_mode not supported in Wx".format(
                    selection_mode
                ),
                RuntimeWarning,
            )
            return
        old_mode = self._get_control_selection_mode()
        if selection_mode != old_mode:
            self.control.ToggleWindowStyle(DV_MULTIPLE)

    def _get_control_selection(self):
        """ Toolkit specific method to get the selection. """
        return [
            (self._item_model._to_row_index(item), ())
            for item in self.control.GetSelections()
        ]

    def _set_control_selection(self, selection):
        """ Toolkit specific method to change the selection. """
        wx_selection = DataViewItemArray()
        for row, column in selection:
            item = self._item_model._to_item(row)
            wx_selection.append(item)
        self.control.SetSelections(wx_selection)
        if wx.VERSION >= (4, 1):
            if len(wx_selection) > 0:
                item = wx_selection[-1]
            else:
                # a dummy item because  we have nothing specific
                item = self._item_model._to_item((0,))
            event = DataViewEvent(
                wxEVT_DATAVIEW_SELECTION_CHANGED,
                self.control,
                item,
            )
        else:
            event = DataViewEvent(
                wxEVT_DATAVIEW_SELECTION_CHANGED,
            )
        wx.PostEvent(self.control, event)

    def _observe_control_selection(self, remove=False):
        """ Toolkit specific method to watch for changes in the selection. """
        if remove:
            self.control.Unbind(
                EVT_DATAVIEW_SELECTION_CHANGED,
                handler=self._update_selection,
            )
        else:
            self.control.Bind(
                EVT_DATAVIEW_SELECTION_CHANGED,
                self._update_selection,
            )

    # ------------------------------------------------------------------------
    # Widget Interface
    # ------------------------------------------------------------------------

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

    def destroy(self):
        """ Perform any actions required to destroy the control. """
        super().destroy()
        # ensure that we release the reference to the item model
        self._item_model = None

    # ------------------------------------------------------------------------
    # Private methods
    # ------------------------------------------------------------------------

    # Trait observers

    @observe('data_model', dispatch='ui')
    def update_item_model(self, event):
        if self._item_model is not None:
            self._item_model.model = event.new
