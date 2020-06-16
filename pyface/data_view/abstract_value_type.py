from abc import abstractmethod
import locale
from math import inf
import sys

from traits.api import (
    ABCHasStrictTraits, Any, Bool, Callable, Enum, Event, Int, Str, Float,
    observe
)
from pyface.ui_traits import Image


default_max = sys.maxsize
default_min = -sys.maxsize + 1


class AbstractValueType(ABCHasStrictTraits):
    """ A value type converts raw data into data channels.

    The data channels are editor value, text, color, image, and description.
    The data channels are used by other parts of the code to produce the actual
    display.
    """

    #: Fired when a change occurs that requires updating values.
    updated = Event

    def is_valid(self, model, row, column, value):
        return True

    def get_is_editable(self, model, row, column):
        return False

    def get_editable(self, model, row, column):
        return model.get_value(row, column)

    def set_editable(self, model, row, column, value):
        return model.set_value(row, column, value)

    def has_text(self, model, row, column):
        return self.get_text(model, row, column) != ""

    def get_text(self, model, row, column):
        return str(model.get_value(row, column))

    def set_text(self, model, row, column, text):
        """ Default behaviour does not allow setting the text. """
        return False

    @observe('+update')
    def update_value_type(self, event=None):
        """ Fire update event when marked traits change. """
        self.updated = True


class BaseValueType(AbstractValueType):

    #: Whether or not there is an editable value.
    is_editable = Bool(True, update=True)

    def get_is_editable(self, model, row, column):
        return self.is_editable

    def get_editable(self, model, row, column):
        return model.get_value(row, column)

    def set_editable(self, model, row, column, value):
        return model.set_value(row, column, value)

    def has_text(self, model, row, column):
        return True

    def get_text(self, model, row, column):
        return self.text

    def set_text(self, model, row, column, text):
        """ Default behaviour does not allow setting the text. """
        return False


class NoneValue(AbstractValueType):

    def is_valid(self, model, row, column, value):
        return True

    def get_is_editable(self, model, row, column):
        return False

    def has_text(self, model, row, column):
        return False


none_value = NoneValue()

class ConstantValueType(AbstractValueType):

    text = Str(update=True)

    def has_text(self, model, row, column):
        return self.text != ""

    def get_text(self, model, row, column):
        return self.text

