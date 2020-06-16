# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase, expectedFailure

from traits.testing.unittest_tools import UnittestTools
from traits.testing.optional_dependencies import numpy as np, requires_numpy

from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.value_types.api import FloatValue, IntValue, TextValue
from ..array_data_model import ArrayDataModel


@requires_numpy
class TestArrayDataModel(UnittestTools, TestCase):

    def setUp(self):
        super().setUp()
        self.array = np.arange(15.0).reshape(5, 3)
        self.model = ArrayDataModel(data=self.array)
        self.values_changed_event = None
        self.structure_changed_event = None
        self.model.observe(self.model_values_changed, 'values_changed')
        self.model.observe(self.model_structure_changed, 'structure_changed')

    def tearDown(self):
        self.model.observe(
            self.model_values_changed, 'values_changed', remove=True)
        self.model.observe(
            self.model_structure_changed, 'structure_changed', remove=True)
        self.values_changed_event = None
        self.structure_changed_event = None
        super().tearDown()

    def model_values_changed(self, event):
        self.values_changed_event = event

    def model_structure_changed(self, event):
        self.structure_changed_event = event

    def test_get_column_count(self):
        for row in self.model.iter_rows():
            with self.subTest(row=row):
                result = self.model.get_column_count(row)
                self.assertEqual(result, 3)

    def test_can_have_children(self):
        for row in self.model.iter_rows():
            with self.subTest(row=row):
                result = self.model.can_have_children(row)
                if len(row) == 0:
                    self.assertEqual(result, True)
                else:
                    self.assertEqual(result, False)

    def test_get_row_count(self):
        for row in self.model.iter_rows():
            with self.subTest(row=row):
                result = self.model.get_row_count(row)
                if len(row) == 0:
                    self.assertEqual(result, 5)
                else:
                    self.assertEqual(result, 0)

    def test_get_value(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                result = self.model.get_value(row, column)
                if row == []:
                    self.assertEqual(result, column[0])
                elif column == []:
                    self.assertEqual(result, row[0])
                else:
                    self.assertEqual(result, self.array[row[0], column[0]])

    def test_set_value(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                if row == []:
                    result = self.model.set_value(row, column, column[0] + 1)
                    self.assertFalse(result)
                elif column == []:
                    result = self.model.set_value(row, column, row[0] + 1)
                    self.assertFalse(result)
                else:
                    value = 6.0 * row[0] + 2 * column[0]
                    with self.assertTraitChanges(self.model, "values_changed"):
                        result = self.model.set_value(row, column, value)
                    self.assertTrue(result)
                    self.assertEqual(self.array[row[0], column[0]], value)
                    self.assertEqual(
                        self.values_changed_event.new,
                        (row, column, row, column)
                    )

    def test_get_value_type(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                result = self.model.get_value_type(row, column)
                if row == []:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.column_header_type)
                elif column == []:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.row_header_type)
                else:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.value_type)

    def test_data_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.data = 2 * self.array
        self.assertEqual(
            self.values_changed_event.new,
            ([0], [0], [5], [3])
        )

    def test_data_updated_new_shape(self):
        with self.assertTraitChanges(self.model, "structure_changed"):
            self.model.data = 2 * self.array.T
        self.assertTrue(self.structure_changed_event.new)

    def test_type_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.value_type = IntValue()
        self.assertEqual(
            self.values_changed_event.new,
            ([0], [0], [5], [3])
        )

    def test_type_attribute_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.value_type.is_editable = False
        self.assertEqual(
            self.values_changed_event.new,
            ([0], [0], [5], [3])
        )

    def test_default_value_type(self):
        data = np.arange(15).reshape(5, 3)
        model = ArrayDataModel(data=data)
        self.assertIsInstance(model.value_type, IntValue)

        data = np.arange(15.0).reshape(5, 3)
        model = ArrayDataModel(data=data)
        self.assertIsInstance(model.value_type, FloatValue)

        data = np.array([['a', 'b', 'c'], ['e', 'f', 'g']])
        model = ArrayDataModel(data=data)
        self.assertIsInstance(model.value_type, TextValue)
