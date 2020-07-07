# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import locale
from math import inf

from traits.api import Callable, Float

from .editable_value import EditableValue


def format_locale(value):
    return "{:n}".format(value)


class NumericValue(EditableValue):
    """ Data channels for a numeric value.
    """

    #: The minimum value for the numeric value.
    minimum = Float(-inf)

    #: The maximum value for the numeric value.
    maximum = Float(inf)

    #: A function that converts to the numeric type.
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

    def get_editor_value(self, model, row, column):
        # evaluate is needed to convert numpy types to python types so
        # Qt recognises them
        return self.evaluate(model.get_value(row, column))

    def get_text(self, model, row, column):
        return self.format(model.get_value(row, column))

    def set_text(self, model, row, column, text):
        try:
            value = self.evaluate(self.unformat(text))
        except ValueError:
            return False
        return self.set_editor_value(model, row, column, value)


class IntValue(NumericValue):

    evaluate = Callable(int)


class FloatValue(NumericValue):

    evaluate = Callable(float)
