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

from pyface.data_view.data_view_errors import (
    DataViewGetError, DataViewSetError
)
from pyface.data_view.index_manager import Root
from wx.dataview import DataViewItem, DataViewModel as wxDataViewModel


logger = logging.getLogger(__name__)


# XXX This file is scaffolding and may need to be rewritten or expanded

class DataViewModel(wxDataViewModel):
    """ A wxDataViewModel that understands AbstractDataModels. """

    def __init__(self, model):
        super().__init__()
        self.model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if hasattr(self, '_model'):
            # disconnect trait listeners
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
            self._model = model
        else:
            # model is being initialized
            self._model = model

        # hook up trait listeners
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

    def on_structure_changed(self, event):
        self.Cleared()

    def on_values_changed(self, event):
        top, left, bottom, right = event.new
        if top == () and bottom == ():
            # this is a column header change, reset everything
            self.Cleared()
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

            if top == bottom and left == right:
                # single value change
                self.ValueChanged(self._to_item(top), left[0])
            elif top == bottom:
                # single item change
                self.ItemChanged(self._to_item(top))
            else:
                # multiple item change
                items = [
                    self._to_item(top[:i] + [row])
                    for row in range(top[i], bottom[i]+1)
                ]
                self.ItemsChanged(items)

    def GetParent(self, item):
        index = self._to_index(item)
        if index == Root:
            return DataViewItem()
        parent, row = self.model.index_manager.get_parent_and_row(index)
        parent_id = self.model.index_manager.id(parent)
        if parent_id == 0:
            return DataViewItem()
        return DataViewItem(parent_id)

    def GetChildren(self, item, children):
        index = self._to_index(item)
        row_index = self.model.index_manager.to_sequence(index)
        n_children = self.model.get_row_count(row_index)
        for i in range(n_children):
            child_index = self.model.index_manager.create_index(index, i)
            child_id = self.model.index_manager.id(child_index)
            children.append(DataViewItem(child_id))
        return n_children

    def IsContainer(self, item):
        row_index = self._to_row_index(item)
        return self.model.can_have_children(row_index)

    def HasValue(self, item, column):
        return True

    def HasChildren(self, item):
        row_index = self._to_row_index(item)
        return self.model.has_child_rows(row_index)

    def GetValue(self, item, column):
        row_index = self._to_row_index(item)
        if column == 0:
            column_index = ()
        else:
            column_index = (column - 1,)
        value_type = self.model.get_value_type(row_index, column_index)
        try:
            if value_type.has_text(self.model, row_index, column_index):
                return value_type.get_text(self.model, row_index, column_index)
        except DataViewGetError:
            return ''
        except Exception:
            # unexpected error, log and raise
            logger.exception(
                "get data failed: row %r, column %r",
                row_index,
                column_index,
            )
            raise
        return ''

    def SetValue(self, value, item, column):
        row_index = self._to_row_index(item)
        if column == 0:
            column_index = ()
        else:
            column_index = (column - 1,)
        try:
            value_type = self.model.get_value_type(row_index, column_index)
            value_type.set_text(self.model, row_index, column_index, value)
        except DataViewSetError:
            return False
        except Exception:
            logger.exception(
                "SetValue failed: row %r, column %r, value %r",
                row_index,
                column_index,
                value,
            )
            return False
        else:
            return True

    def GetColumnCount(self):
        return self.model.get_column_count() + 1

    def GetColumnType(self, column):
        # XXX This may need refinement when we deal with different editor types
        return "string"

    def _to_row_index(self, item):
        id = item.GetID()
        if id is None:
            id = 0
        index = self.model.index_manager.from_id(int(id))
        return self.model.index_manager.to_sequence(index)

    def _to_item(self, row_index):
        if len(row_index) == 0:
            return DataViewItem()
        index = self.model.index_manager.from_sequence(row_index)
        id = self.model.index_manager.id(index)
        return DataViewItem(id)

    def _to_index(self, item):
        id = item.GetID()
        if id is None:
            id = 0
        return self.model.index_manager.from_id(int(id))
