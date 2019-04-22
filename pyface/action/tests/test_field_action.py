# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from pyface.fields.api import ComboField, SpinField, TextField
from pyface.window import Window
from ..field_action import FieldAction


class TestFieldAction(unittest.TestCase):

    def setUp(self):
        self.parent = Window()
        self.parent._create()
        self.addCleanup(self._destroy_parent)

    def _destroy_parent(self):
        self.parent.destroy()
        self.parent = None

    def test_combo_field_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform(value):
            memo.append(value)

        action = FieldAction(
            name="Dummy",
            field_type=ComboField,
            field_defaults={
                'values': ['a', 'b', 'c'],
                'value': 'a',
                'tooltip': 'Dummy',
            },
            on_perform=perform,
        )
        control = action.create_control(self.parent.control)
        try:
            control._field.value = 'b'

            self.assertEqual(memo, ['b'])
        finally:
            control._field.destroy()

    def test_text_field_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform(value):
            memo.append(value)

        action = FieldAction(
            name="Dummy",
            field_type=TextField,
            field_defaults={
                'value': 'a',
                'tooltip': 'Dummy',
            },
            on_perform=perform,
        )
        control = action.create_control(self.parent.control)

        try:
            control._field.value = 'b'

            self.assertEqual(memo, ['b'])
        finally:
            control._field.destroy()

    def test_spin_field_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform(value):
            memo.append(value)

        action = FieldAction(
            name="Dummy",
            field_type=SpinField,
            field_defaults={
                'value': 1,
                'bounds': (0, 100),
                'tooltip': 'Dummy',
            },
            on_perform=perform,
        )
        control = action.create_control(self.parent.control)

        try:
            control._field.value = 5

            self.assertEqual(memo, [5])
        finally:
            control._field.destroy()
