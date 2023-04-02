# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase
from unittest.mock import Mock

from pyface.data_view.data_view_errors import DataViewSetError
from pyface.data_view.value_types.numeric_value import (
    FloatValue, IntValue, NumericValue, format_locale
)


class TestNumericValue(TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value=1.0)
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock(return_value=True)

    def test_defaults(self):
        value = NumericValue()
        self.assertIsNone(value.evaluate)

    def test_is_valid(self):
        value = NumericValue()
        self.assertTrue(value.is_valid(None, [0], [0], 0.0))

    def test_is_valid_false(self):
        value = NumericValue(minimum=0.0, maximum=1.0)
        self.assertFalse(value.is_valid(None, [0], [0], -1.0))

    def test_is_valid_error(self):
        value = NumericValue()
        self.assertFalse(value.is_valid(None, [0], [0], 'invalid'))

    def test_get_editor_value(self):
        value = NumericValue(evaluate=float)
        editable = value.get_editor_value(self.model, [0], [0])

        self.assertEqual(editable, 1.0)

    def test_set_editor_value(self):
        value = NumericValue(evaluate=float)
        value.set_editor_value(self.model, [0], [0], 1.0)
        self.model.set_value.assert_called_once_with([0], [0], 1.0)

    def test_set_editor_value_invalid(self):
        value = NumericValue(minimum=0.0, maximum=1.0)
        with self.assertRaises(DataViewSetError):
            value.set_editor_value(self.model, [0], [0], -1.0)
        self.model.set_value.assert_not_called()

    def test_set_editor_value_error(self):
        value = NumericValue(minimum=0.0, maximum=1.0)
        with self.assertRaises(DataViewSetError):
            value.set_editor_value(self.model, [0], [0], 'invalid')
        self.model.set_value.assert_not_called()

    def test_get_text(self):
        value = NumericValue()
        text = value.get_text(self.model, [0], [0])
        self.assertEqual(text, format_locale(1.0))

    def test_set_text(self):
        value = NumericValue(evaluate=float)
        value.set_text(self.model, [0], [0], format_locale(1.1))
        self.model.set_value.assert_called_once_with([0], [0], 1.1)

    def test_set_text_invalid(self):
        value = NumericValue(evaluate=float, minimum=0.0, maximum=1.0)
        with self.assertRaises(DataViewSetError):
            value.set_text(self.model, [0], [0], format_locale(1.1))
        self.model.set_value.assert_not_called()

    def test_set_text_error(self):
        value = NumericValue(evaluate=float)
        with self.assertRaises(DataViewSetError):
            value.set_text(self.model, [0], [0], "invalid")
        self.model.set_value.assert_not_called()


class TestIntValue(TestCase):

    def test_defaults(self):
        value = IntValue()
        self.assertIs(value.evaluate, int)


class TestFloatValue(TestCase):

    def test_defaults(self):
        value = FloatValue()
        self.assertIs(value.evaluate, float)
