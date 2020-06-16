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

from ..constant_value import ConstantValue


class TestConstantValue(UnittestTools, TestCase):

    def setUp(self):
        self.model = Mock()

    def test_defaults(self):
        value_type = ConstantValue()
        self.assertEqual(value_type.text, "")

    def test_can_edit(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.can_edit(self.model, [0], [0]))

    def test_has_text(self):
        value_type = ConstantValue()
        self.assertFalse(value_type.has_text(self.model, [0], [0]))

    def test_has_text_true(self):
        value_type = ConstantValue(text="something")
        self.assertTrue(value_type.has_text(self.model, [0], [0]))

    def test_get_text(self):
        value_type = ConstantValue(text="something")
        self.assertEqual(value_type.get_text(self.model, [0], [0]), "something")

    def test_text_changed(self):
        value_type = ConstantValue()
        with self.assertTraitChanges(value_type, 'updated'):
            value_type.text = 'something'
        self.assertEqual(value_type.text, 'something')
