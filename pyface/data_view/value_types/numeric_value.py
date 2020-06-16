import locale
from math import inf

from traits.api import (
    Bool, Callable, Enum, Event, Int, Str, Float,
    observe
)

from pyface.data_view.abstract_value_type import BaseValueType


def format_locale(value):
    return "{:n}".format(value)


class NumericValue(BaseValueType):
    """ Data channels for a numeric value.
    """

    #: The minimum value for the numeric value.
    minimum = Float(-inf)

    #: The maximum value for the numeric value.
    maximum = Float(inf)

    #: A function that converts to the a numeric type.
    evaluate = Callable()

    #: A function that converts the required type to a string for display.
    format = Callable(format_locale, update=True)

    #: A function that converts the required type from a display string.
    unformat = Callable(locale.delocalize)

    def is_valid(self, model, row, column, value):
        try:
            return self.minimum <= value <= self.maximum
        except Exception:
            return False

    def get_editable(self, model, row, column):
        # evaluate is needed to convert numpy types to python types so
        # Qt recognises them
        return self.evaluate(model.get_value(row, column))

    def set_editable(self, model, row, column, value):
        if not self.is_valid(model, row, column, value):
            return False
        return model.set_value(row, column, value)

    def get_text(self, model, row, column):
        return self.format(model.get_value(row, column))

    def set_text(self, model, row, column, text):
        try:
            value = self.evaluate(self.unformat(text))
        except ValueError:
            return False
        return self.set_editable(model, row, column, value)


class IntValue(NumericValue):

    evaluate = Callable(int)


class FloatValue(NumericValue):

    evaluate = Callable(float)


class ProportionValue(NumericValue):

    minimum = 0.0

    maximum = 1.0

    evaluate = Callable(float)
