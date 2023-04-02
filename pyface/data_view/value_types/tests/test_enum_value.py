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
from pyface.data_view.value_types.enum_value import EnumValue


class TestEnumValue(TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value=1)
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock()

    def test_defaults(self):
        value = EnumValue()
        self.assertTrue(value.is_editable)

    def test_is_valid(self):
        value = EnumValue(values=[1, 2])
        self.assertTrue(value.is_valid(None, [0], [0], 1))

    def test_is_valid_false(self):
        value = EnumValue(values=[2])
        self.assertFalse(value.is_valid(None, [0], [0], 1))

    def test_get_editor_value(self):
        value = EnumValue()
        editable = value.get_editor_value(self.model, [0], [0])
        self.assertEqual(editable, 1)

    def test_set_editor_value(self):
        value = EnumValue(values=[1, 2])
        value.set_editor_value(self.model, [0], [0], 2)
        self.model.set_value.assert_called_once_with([0], [0], 2)

    def test_set_editor_value_bad(self):
        value = EnumValue(values=[1])
        with self.assertRaises(DataViewSetError):
            value.set_editor_value(self.model, [0], [0], 2)

    def test_has_text(self):
        value = EnumValue(values=[1, 2])
        has_text = value.has_text(self.model, [0], [0])
        self.assertTrue(has_text)

    def test_has_text_false(self):
        value = EnumValue(values=[1, 2], format=None)
        has_text = value.has_text(self.model, [0], [0])
        self.assertFalse(has_text)

    def test_get_text(self):
        value = EnumValue(values=[1, 2])
        text = value.get_text(self.model, [0], [0])
        self.assertEqual(text, "1")

    def test_has_color_false(self):
        value = EnumValue(values=[1, 2])
        has_color = value.has_color(self.model, [0], [0])
        self.assertFalse(has_color)

    def test_has_color_true(self):
        value = EnumValue(values=[1, 2], colors=lambda x: "dummy")
        has_color = value.has_color(self.model, [0], [0])
        self.assertTrue(has_color)

    def test_get_color(self):
        value = EnumValue(values=[1, 2], colors=lambda x: "dummy")
        color = value.get_color(self.model, [0], [0])
        self.assertEqual(color, "dummy")

    def test_color_function_none(self):
        value = EnumValue(values=[1, 2], colors=lambda x: None)
        has_color = value.has_color(self.model, [0], [0])
        self.assertTrue(has_color)
        color = value.get_color(self.model, [0], [0])
        self.assertIsNone(color)

    def test_has_image_false(self):
        value = EnumValue(values=[1, 2])
        has_image = value.has_image(self.model, [0], [0])
        self.assertFalse(has_image)

    def test_has_image_true(self):
        value = EnumValue(values=[1, 2], images=lambda x: "dummy")
        has_image = value.has_image(self.model, [0], [0])
        self.assertTrue(has_image)

    def test_get_image(self):
        value = EnumValue(values=[1, 2], images=lambda x: "dummy")
        image = value.get_image(self.model, [0], [0])
        self.assertEqual(image, "dummy")

    def test_image_function_none(self):
        value = EnumValue(values=[1, 2], images=lambda x: None)
        has_image = value.has_image(self.model, [0], [0])
        self.assertTrue(has_image)
        image = value.get_image(self.model, [0], [0])
        self.assertIsNone(image)
