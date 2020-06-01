

from pyface.data_view.index_manager import Root
from wx.dataview import DataViewItem, DataViewModel as wxDataViewModel


# XXX This file is scaffolding and may need to be rewritten or expanded

class DataViewModel(wxDataViewModel):

    def __init__(self, model):
        super().__init__()
        self._model = model

    @property
    def model(self):
        return self._model

    def GetParent(self, item):
        index = self._to_index(item)
        if index == Root:
            return None
        parent, row = self.model.index_manager.get_parent_and_row(index)
        parent_id = self.model.index_manager.id(parent)
        if parent_id == 0:
            return None
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

    def HasContainerColumns(self, item):
        return item.GetID() is not None

    def HasChildren(self, item):
        row_index = self._to_row_index(item)
        return self.model.has_child_rows(row_index)

    def GetValue(self, item, column):
        row_index = self._to_row_index(item)
        column_index = [column]
        value = self.model.get_text(row_index, column_index)
        return value

    def SetValue(self, value, item, column):
        row_index = self._to_row_index(item)
        column_index = [column]
        try:
            self.model.set_text(row_index, column_index, value)
        except Exception as exc:
            print(exc)
            # XXX log it
            return False
        return True

    def GetColumnCount(self):
        return self.model.get_column_count([])

    def _to_row_index(self, item):
        id = item.GetID()
        if id is None:
            id = -1
        index = self.model.index_manager.from_id(id)
        return self.model.index_manager.to_sequence(index)

    def _to_index(self, item):
        id = item.GetID()
        if id is None:
            id = 0
        return self.model.index_manager.from_id(id)
