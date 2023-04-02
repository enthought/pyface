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

from pyface.data_view.abstract_value_type import CheckState
from pyface.data_view.data_view_errors import DataViewSetError
from pyface.data_view.value_types.bool_value import BoolValue


class TestBoolValue(TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value=True)
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock()

    def test_defaults(self):
        value = BoolValue()
        self.assertEqual(value.true_text, "")
        self.assertEqual(value.false_text, "")

    def test_has_text_default(self):
        value = BoolValue()
        has_text = value.has_text(self.model, [0], [0])
        self.assertFalse(has_text)

    def test_has_text(self):
        value = BoolValue(true_text="Yes", false_text="No")
        has_text = value.has_text(self.model, [0], [0])
        self.assertTrue(has_text)

    def test_get_text_default(self):
        value = BoolValue()
        text = value.get_text(self.model, [0], [0])
        self.assertEqual(text, "")

        self.model.get_value = Mock(return_value=False)
        text = value.get_text(self.model, [0], [0])
        self.assertEqual(text, "")

    def test_get_text(self):
        value = BoolValue(true_text="Yes", false_text="No")
        text = value.get_text(self.model, [0], [0])
        self.assertEqual(text, "Yes")

        self.model.get_value = Mock(return_value=False)
        text = value.get_text(self.model, [0], [0])
        self.assertEqual(text, "No")

    def test_get_check_state(self):
        value = BoolValue()
        check_state = value.get_check_state(self.model, [0], [0])
        self.assertEqual(check_state, CheckState.CHECKED)

    def test_get_check_state_false(self):
        value = BoolValue()
        self.model.get_value = Mock(return_value=False)
        check_state = value.get_check_state(self.model, [0], [0])
        self.assertEqual(check_state, CheckState.UNCHECKED)

    def test_set_check_state(self):
        value = BoolValue()
        value.set_check_state(self.model, [0], [0], CheckState.CHECKED)
        self.model.set_value.assert_called_once_with([0], [0], True)

    def test_set_check_state_unchecked(self):
        value = BoolValue()
        value.set_check_state(self.model, [0], [0], CheckState.UNCHECKED)
        self.model.set_value.assert_called_once_with([0], [0], False)

    def test_set_check_state_no_set_value(self):
        self.model.can_set_value = Mock(return_value=False)
        value = BoolValue()
        with self.assertRaises(DataViewSetError):
            value.set_text(self.model, [0], [0], CheckState.CHECKED)
