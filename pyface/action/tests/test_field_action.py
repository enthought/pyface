from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from pyface.fields.api import ComboField, SpinField, TextField
from ..field_action import FieldAction


class TestFieldAction(unittest.TestCase):

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
        parent = None
        control = action.create_control(parent)

        control._field.value = 'b'

        self.assertEqual(memo, ['b'])

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
        parent = None
        control = action.create_control(parent)

        control._field.value = 'b'

        self.assertEqual(memo, ['b'])

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
        parent = None
        control = action.create_control(parent)

        control._field.value = 5

        self.assertEqual(memo, [5])
