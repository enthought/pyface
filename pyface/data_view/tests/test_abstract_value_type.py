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

from traits.api import Str
from traits.testing.api import UnittestTools

from pyface.color import Color
from pyface.data_view.data_view_errors import DataViewSetError
from pyface.data_view.abstract_value_type import AbstractValueType, CheckState


class ValueType(AbstractValueType):

    #: a parameter which should fire the update trait
    sample_parameter = Str(update_value_type=True)


class TestAbstractValueType(UnittestTools, TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value=1.0)
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock()

    def test_has_editor_value(self):
        value_type = ValueType()
        result = value_type.has_editor_value(self.model, [0], [0])
        self.assertTrue(result)

    def test_has_editor_value_can_set_value_false(self):
        self.model.can_set_value = Mock(return_value=False)
        value_type = ValueType()
        result = value_type.has_editor_value(self.model, [0], [0])
        self.assertFalse(result)

    def test_get_editor_value(self):
        value_type = ValueType()
        result = value_type.get_editor_value(self.model, [0], [0])
        self.assertEqual(result, 1.0)

    def test_set_editor_value(self):
        value_type = ValueType()
        value_type.set_editor_value(self.model, [0], [0], 2.0)
        self.model.set_value.assert_called_once_with([0], [0], 2.0)

    def test_set_editor_value_set_value_raises(self):
        self.model.set_value = Mock(side_effect=DataViewSetError)
        value_type = ValueType()
        with self.assertRaises(DataViewSetError):
            value_type.set_editor_value(self.model, [0], [0], 2.0)
        self.model.set_value.assert_called_once_with([0], [0], 2.0)

    def test_has_text(self):
        value_type = ValueType()
        result = value_type.has_text(self.model, [0], [0])
        self.assertTrue(result)

    def test_get_text(self):
        value_type = ValueType()
        result = value_type.get_text(self.model, [0], [0])
        self.assertEqual(result, "1.0")

    def test_set_text(self):
        value_type = ValueType()
        with self.assertRaises(DataViewSetError):
            value_type.set_text(self.model, [0], [0], "2.0")

    def test_has_color(self):
        value_type = ValueType()
        result = value_type.has_color(self.model, [0], [0])
        self.assertFalse(result)

    def test_get_color(self):
        value_type = ValueType()
        result = value_type.get_color(self.model, [0], [0])
        self.assertEqual(result, Color(rgb=(1.0, 1.0, 1.0)))

    def test_has_image(self):
        value_type = ValueType()
        result = value_type.has_image(self.model, [0], [0])
        self.assertFalse(result)

    def test_get_image(self):
        value_type = ValueType()
        result = value_type.get_image(self.model, [0], [0])
        self.assertEqual(result.name, "image_not_found")

    def test_has_check_state(self):
        value_type = ValueType()
        result = value_type.has_check_state(self.model, [0], [0])
        self.assertFalse(result)

    def test_get_check_state(self):
        value_type = ValueType()
        result = value_type.get_check_state(self.model, [0], [0])
        self.assertEqual(result, CheckState.CHECKED)

    def test_set_check_state(self):
        value_type = ValueType()
        with self.assertRaises(DataViewSetError):
            value_type.set_check_state(self.model, [0], [0], CheckState.CHECKED)

    def test_parameter_update(self):
        value_type = ValueType()
        with self.assertTraitChanges(value_type, 'updated', count=1):
            value_type.sample_parameter = "new value"
