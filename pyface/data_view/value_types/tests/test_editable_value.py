# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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

from traits.testing.unittest_tools import UnittestTools

from pyface.data_view.value_types.editable_value import EditableValue


class EditableWithValid(EditableValue):

    def is_valid(self, model, row, column, value):
        return value >= 0


class TestEditableValue(UnittestTools, TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value=1.0)
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock(return_value=True)

    def test_default(self):
        value_type = EditableValue()
        self.assertTrue(value_type.is_editable)

    def test_is_valid(self):
        value_type = EditableValue()
        result = value_type.is_valid(self.model, [0], [0], 2.0)
        self.assertTrue(result)

    def test_can_edit(self):
        value_type = EditableValue()
        result = value_type.can_edit(self.model, [0], [0])
        self.assertTrue(result)

    def test_can_edit_not_editable(self):
        value_type = EditableValue(is_editable=False)
        result = value_type.can_edit(self.model, [0], [0])
        self.assertFalse(result)

    def test_set_editable(self):
        value_type = EditableValue()
        result = value_type.set_editable(self.model, [0], [0], 2.0)
        self.assertTrue(result)

    def test_set_editable_not_editable(self):
        value_type = EditableValue(is_editable=False)
        result = value_type.set_editable(self.model, [0], [0], 2.0)
        self.assertFalse(result)

    def test_set_editable_not_valid(self):
        value_type = EditableWithValid()
        result = value_type.set_editable(self.model, [0], [0], -1.0)
        self.assertFalse(result)

    def test_is_editable_update(self):
        value_type = EditableValue()
        with self.assertTraitChanges(value_type, 'updated', count=1):
            value_type.is_editable = False
