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

from pyface.color import Color
from pyface.data_view.abstract_data_model import DataViewSetError
from pyface.data_view.value_types.color_value import ColorValue


class TestColorValue(TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(
            return_value=Color(rgba=(0.4, 0.2, 0.6, 0.8)),
        )
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock()

    def test_defaults(self):
        value = ColorValue()
        self.assertTrue(value.is_editable)

    def test_is_valid(self):
        value = ColorValue()
        self.assertTrue(value.is_valid(None, [0], [0], Color()))

    def test_get_editor_value(self):
        value = ColorValue()
        editable = value.get_editor_value(self.model, [0], [0])
        self.assertEqual(editable, "#663399CC")

    def test_set_editor_value(self):
        value = ColorValue()
        value.set_editor_value(self.model, [0], [0], "#3399CC66")
        self.model.set_value.assert_called_once_with(
            [0],
            [0],
            Color(rgba=(0.2, 0.6, 0.8, 0.4)),
        )

    def test_get_text(self):
        value = ColorValue()
        editable = value.get_text(self.model, [0], [0])
        self.assertEqual(editable, "#663399CC")

    def test_set_text(self):
        value = ColorValue()
        value.set_text(self.model, [0], [0], "red")
        self.model.set_value.assert_called_once_with(
            [0],
            [0],
            Color(rgba=(1.0, 0.0, 0.0, 1.0)),
        )

    def test_set_text_error(self):
        value = ColorValue()
        with self.assertRaises(DataViewSetError):
            value.set_text(self.model, [0], [0], "not a real color")

    def test_set_text_no_set_value(self):
        self.model.can_set_value = Mock(return_value=False)
        value = ColorValue()
        value.set_text(self.model, [0], [0], "red")
        self.model.set_value.assert_called_once_with(
            [0],
            [0],
            Color(rgba=(1.0, 0.0, 0.0, 1.0)),
        )

    def test_get_color(self):
        value = ColorValue()
        editable = value.get_color(self.model, [0], [0])
        self.assertEqual(editable, Color(rgba=(0.4, 0.2, 0.6, 0.8)))
