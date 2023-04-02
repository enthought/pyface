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

from traits.testing.api import UnittestTools

from pyface.data_view.data_view_errors import DataViewSetError
from pyface.data_view.value_types.editable_value import EditableValue


class EditableWithValid(EditableValue):

    def is_valid(self, model, row, column, value):
        return value >= 0


class TestEditableValue(UnittestTools, TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value=1.0)
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock()

    def test_default(self):
        value_type = EditableValue()
        self.assertTrue(value_type.is_editable)

    def test_is_valid(self):
        value_type = EditableValue()
        result = value_type.is_valid(self.model, [0], [0], 2.0)
        self.assertTrue(result)

    def test_has_editor_value(self):
        value_type = EditableValue()
        result = value_type.has_editor_value(self.model, [0], [0])
        self.assertTrue(result)

    def test_has_editor_value_not_editable(self):
        value_type = EditableValue(is_editable=False)
        result = value_type.has_editor_value(self.model, [0], [0])
        self.assertFalse(result)

    def test_set_editor_value(self):
        value_type = EditableValue()
        value_type.set_editor_value(self.model, [0], [0], 2.0)
        self.model.set_value.assert_called_once_with([0], [0], 2.0)

    def test_set_editor_value_set_value_raises(self):
        self.model.set_value = Mock(side_effect=DataViewSetError)
        value_type = EditableValue(is_editable=False)
        with self.assertRaises(DataViewSetError):
            value_type.set_editor_value(self.model, [0], [0], 2.0)
        self.model.set_value.assert_called_once_with([0], [0], 2.0)

    def test_set_editor_value_not_valid(self):
        value_type = EditableWithValid()
        with self.assertRaises(DataViewSetError):
            value_type.set_editor_value(self.model, [0], [0], -1.0)
        self.model.set_value.assert_not_called()

    def test_is_editable_update(self):
        value_type = EditableValue()
        with self.assertTraitChanges(value_type, 'updated', count=1):
            value_type.is_editable = False
