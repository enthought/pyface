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

from pyface.data_view.value_types.text_value import TextValue


class TestTextValue(TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value="test")
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock()

    def test_defaults(self):
        value = TextValue()
        self.assertTrue(value.is_editable)

    def test_is_valid(self):
        value = TextValue()
        self.assertTrue(value.is_valid(None, [0], [0], "test"))

    def test_get_editor_value(self):
        value = TextValue()
        editable = value.get_editor_value(self.model, [0], [0])
        self.assertEqual(editable, "test")

    def test_set_editor_value(self):
        value = TextValue()
        value.set_editor_value(self.model, [0], [0], "test")
        self.model.set_value.assert_called_once_with([0], [0], "test")

    def test_get_text(self):
        value = TextValue()
        editable = value.get_text(self.model, [0], [0])
        self.assertEqual(editable, "test")

    def test_set_text(self):
        value = TextValue()
        value.set_text(self.model, [0], [0], "test")
        self.model.set_value.assert_called_once_with([0], [0], "test")

    def test_set_text_no_set_value(self):
        self.model.can_set_value = Mock(return_value=False)
        value = TextValue()
        value.set_text(self.model, [0], [0], "test")
        self.model.set_value.assert_called_once_with([0], [0], "test")
