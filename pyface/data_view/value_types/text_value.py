
from pyface.data_view.abstract_value_type import BaseValueType


class TextValue(BaseValueType):

    def get_text(self, model, row, column):
        return str(model.get_value(row, column))

    def set_text(self, model, row, column, text):
        return model.set_value(row, column, text)
