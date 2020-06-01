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

from traits.testing.unittest_tools import UnittestTools
from traits.testing.optional_dependencies import numpy as np, requires_numpy

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
        for row in range(5):
            with self.subTest(row=row):
                result = self.model.get_column_count([row])
                self.assertEqual(result, 3)

    def test_get_column_count_root(self):
        result = self.model.get_column_count([])
        self.assertEqual(result, 3)

    def test_can_have_children(self):
        for row in range(5):
            with self.subTest(row=row):
                result = self.model.can_have_children([row])
                self.assertEqual(result, False)

    def test_can_have_children_root(self):
        result = self.model.can_have_children([])
        self.assertEqual(result, True)

    def test_get_row_count(self):
        for row in range(5):
            with self.subTest(row=row):
                result = self.model.get_row_count([row])
                self.assertEqual(result, 0)

    def test_get_row_count_root(self):
        result = self.model.get_row_count([])
        self.assertEqual(result, 5)

    def test_get_value(self):
        for row in range(5):
            for column in range(3):
                with self.subTest(row=row, column=column):
                    result = self.model.get_value([row], [column])
                    self.assertEqual(result, self.array[row, column])

    def test_get_value_root(self):
        for column in range(3):
            with self.subTest(column=column):
                result = self.model.get_value([], [column])
                self.assertEqual(result, column)

    def test_set_value_float(self):
        for row in range(5):
            for column in range(3):
                with self.subTest(row=row, column=column):
                    value = 6.0 * row + 2 * column
                    with self.assertTraitChanges(self.model, "values_changed"):
                        result = self.model.set_value([row], [column], value)
                    self.assertTrue(result, self.array[row, column])
                    self.assertEqual(self.array[row, column], value)
                    self.assertEqual(
                        self.values_changed_event.new,
                        (([row], [column]), ([row], [column]))
                    )

    def test_set_value_root(self):
        for column in range(3):
            with self.subTest(column=column):
                result = self.model.set_value([], [column], column+1)
                self.assertEqual(result, False)

    def test_get_text(self):
        for row in range(5):
            for column in range(3):
                with self.subTest(row=row, column=column):
                    result = self.model.get_text([row], [column])
                    self.assertEqual(result, str(self.array[row, column]))

    def test_set_value_root(self):
        for column in range(3):
            with self.subTest(column=column):
                result = self.model.set_text([], [column], str(column+1))
                self.assertEqual(result, False)

    def test_set_text_root(self):
        for row in range(5):
            for column in range(3):
                with self.subTest(row=row, column=column):
                    result = self.model.get_text([row], [column])
                    self.assertEqual(result, str(self.array[row, column]))

    def test_set_text_float(self):
        for row in range(5):
            for column in range(3):
                with self.subTest(row=row, column=column):
                    value = 6.0 * row + 2 * column
                    text = str(value)
                    with self.assertTraitChanges(self.model, "values_changed"):
                        result = self.model.set_text([row], [column], text)
                    self.assertTrue(result, self.array[row, column])
                    self.assertEqual(self.array[row, column], value)
                    self.assertEqual(
                        self.values_changed_event.new,
                        (([row], [column]), ([row], [column]))
                    )

    def test_data_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.data = 2*self.array
        self.assertEqual(
            self.values_changed_event.new,
            (([0], [0]), ([5], [3]))
        )

    def test_data_updated_new_shape(self):
        with self.assertTraitChanges(self.model, "structure_changed"):
            self.model.data = 2*self.array.T
        self.assertTrue(self.structure_changed_event.new)
