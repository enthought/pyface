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

from pyface.util.testing import (
    is_traits_version_ge,
    requires_traits_min_version,
)

if is_traits_version_ge("6.1"):
    from pyface.data_view.abstract_data_model import DataViewSetError
    from pyface.data_view.abstract_value_type import AbstractValueType
    from pyface.data_view.value_types.api import (
        FloatValue, IntValue, no_value
    )
    from pyface.data_view.data_models.array_data_model import ArrayDataModel


@requires_traits_min_version("6.1")
@requires_numpy
class TestArrayDataModel(UnittestTools, TestCase):

    def setUp(self):
        super().setUp()
        self.array = np.arange(30.0).reshape(5, 2, 3)
        self.model = ArrayDataModel(data=self.array, value_type=FloatValue())
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

    def test_no_data(self):
        model = ArrayDataModel(value_type=FloatValue())
        self.assertEqual(model.data.ndim, 2)
        self.assertEqual(model.data.shape, (0, 0))
        self.assertEqual(model.data.dtype, np.float)
        self.assertEqual(model.get_column_count(), 0)
        self.assertTrue(model.can_have_children(()))
        self.assertEqual(model.get_row_count(()), 0)

    def test_data_1d(self):
        array = np.arange(30.0)
        model = ArrayDataModel(data=array, value_type=FloatValue())
        self.assertEqual(model.data.ndim, 2)
        self.assertEqual(model.data.shape, (30, 1))

    def test_data_list(self):
        data = list(range(30))
        model = ArrayDataModel(data=data, value_type=FloatValue())
        self.assertEqual(model.data.ndim, 2)
        self.assertEqual(model.data.shape, (30, 1))

    def test_set_data_1d(self):
        with self.assertTraitChanges(self.model, 'structure_changed'):
            self.model.data = np.arange(30.0)
        self.assertEqual(self.model.data.ndim, 2)
        self.assertEqual(self.model.data.shape, (30, 1))

    def test_set_data_list(self):
        with self.assertTraitChanges(self.model, 'structure_changed'):
            self.model.data = list(range(30))
        self.assertEqual(self.model.data.ndim, 2)
        self.assertEqual(self.model.data.shape, (30, 1))

    def test_get_column_count(self):
        result = self.model.get_column_count()
        self.assertEqual(result, 3)

    def test_can_have_children(self):
        for row in self.model.iter_rows():
            with self.subTest(row=row):
                result = self.model.can_have_children(row)
                if len(row) <= 1:
                    self.assertEqual(result, True)
                else:
                    self.assertEqual(result, False)

    def test_get_row_count(self):
        for row in self.model.iter_rows():
            with self.subTest(row=row):
                result = self.model.get_row_count(row)
                if len(row) == 0:
                    self.assertEqual(result, 5)
                elif len(row) == 1:
                    self.assertEqual(result, 2)
                else:
                    self.assertEqual(result, 0)

    def test_get_value(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                result = self.model.get_value(row, column)
                if len(row) == 0 and len(column) == 0:
                    self.assertIsNone(result)
                elif len(row) == 0:
                    self.assertEqual(result, column[0])
                elif len(column) == 0:
                    self.assertEqual(result, row[-1])
                elif len(row) == 1:
                    self.assertIsNone(result)
                else:
                    self.assertEqual(
                        result,
                        self.array[row[0], row[1], column[0]]
                    )

    def test_set_value(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                if len(row) == 0 and len(column) == 0:
                    with self.assertRaises(DataViewSetError):
                        self.model.set_value(row, column, 0)
                elif len(row) == 0:
                    with self.assertRaises(DataViewSetError):
                        self.model.set_value(row, column, column[0] + 1)
                elif len(column) == 0:
                    with self.assertRaises(DataViewSetError):
                        self.model.set_value(row, column, row[-1] + 1)
                elif len(row) == 1:
                    value = 6.0 * row[-1] + 2 * column[0]
                    with self.assertTraitDoesNotChange(
                            self.model, "values_changed"):
                        with self.assertRaises(DataViewSetError):
                            self.model.set_value(row, column, value)
                else:
                    value = 6.0 * row[-1] + 2 * column[0]
                    with self.assertTraitChanges(self.model, "values_changed"):
                        self.model.set_value(row, column, value)
                    self.assertEqual(
                        self.array[row[0], row[1], column[0]],
                        value,
                    )
                    self.assertEqual(
                        self.values_changed_event.new,
                        (row, column, row, column)
                    )

    def test_get_value_type(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                result = self.model.get_value_type(row, column)
                if len(row) == 0 and len(column) == 0:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.label_header_type)
                elif len(row) == 0:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.column_header_type)
                elif len(column) == 0:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.row_header_type)
                elif len(row) == 1:
                    self.assertIs(result, no_value)
                else:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(result, self.model.value_type)

    def test_data_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.data = 2 * self.array
        self.assertEqual(
            self.values_changed_event.new,
            ((0,), (0,), (4,), (2,))
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
            ((0,), (0,), (4,), (2,))
        )

    def test_type_attribute_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.value_type.is_editable = False
        self.assertEqual(
            self.values_changed_event.new,
            ((0,), (0,), (4,), (2,))
        )

    def test_row_header_type_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.row_header_type = no_value
        self.assertEqual(
            self.values_changed_event.new,
            ((0,), (), (4,), ())
        )

    def test_row_header_attribute_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.row_header_type.format = str
        self.assertEqual(
            self.values_changed_event.new,
            ((0,), (), (4,), ())
        )

    def test_column_header_type_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.column_header_type = no_value
        self.assertEqual(
            self.values_changed_event.new,
            ((), (0,), (), (2,))
        )

    def test_column_header_type_attribute_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.column_header_type.format = str
        self.assertEqual(
            self.values_changed_event.new,
            ((), (0,), (), (2,))
        )

    def test_label_header_type_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.label_header_type = no_value
        self.assertEqual(
            self.values_changed_event.new,
            ((), (), (), ())
        )

    def test_label_header_type_attribute_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.label_header_type.text = "My Table"
        self.assertEqual(
            self.values_changed_event.new,
            ((), (), (), ())
        )

    def test_iter_rows(self):
        result = list(self.model.iter_rows())
        self.assertEqual(
            result,
            [
                (),
                (0,),
                (0, 0),
                (0, 1),
                (1,),
                (1, 0),
                (1, 1),
                (2,),
                (2, 0),
                (2, 1),
                (3,),
                (3, 0),
                (3, 1),
                (4,),
                (4, 0),
                (4, 1),
            ]
        )

    def test_iter_rows_start(self):
        result = list(self.model.iter_rows((2,)))
        self.assertEqual(
            result,
            [(2,), (2, 0), (2, 1)]
        )

    def test_iter_rows_leaf(self):
        result = list(self.model.iter_rows([2, 0]))
        self.assertEqual(result, [(2, 0)])

    def test_iter_items(self):
        result = list(self.model.iter_items())
        self.assertEqual(
            result,
            [
                ((), ()),
                ((), (0,)), ((), (1,)), ((), (2,)),
                ((0,), ()),
                ((0,), (0,)), ((0,), (1,)), ((0,), (2,)),
                ((0, 0), ()),
                ((0, 0), (0,)), ((0, 0), (1,)), ((0, 0), (2,)),
                ((0, 1), ()),
                ((0, 1), (0,)), ((0, 1), (1,)), ((0, 1), (2,)),
                ((1,), ()),
                ((1,), (0,)), ((1,), (1,)), ((1,), (2,)),
                ((1, 0), ()),
                ((1, 0), (0,)), ((1, 0), (1,)), ((1, 0), (2,)),
                ((1, 1), ()),
                ((1, 1), (0,)), ((1, 1), (1,)), ((1, 1), (2,)),
                ((2,), ()),
                ((2,), (0,)), ((2,), (1,)), ((2,), (2,)),
                ((2, 0), ()),
                ((2, 0), (0,)), ((2, 0), (1,)), ((2, 0), (2,)),
                ((2, 1), ()),
                ((2, 1), (0,)), ((2, 1), (1,)), ((2, 1), (2,)),
                ((3,), ()),
                ((3,), (0,)), ((3,), (1,)), ((3,), (2,)),
                ((3, 0), ()),
                ((3, 0), (0,)), ((3, 0), (1,)), ((3, 0), (2,)),
                ((3, 1), ()),
                ((3, 1), (0,)), ((3, 1), (1,)), ((3, 1), (2,)),
                ((4,), ()),
                ((4,), (0,)), ((4,), (1,)), ((4,), (2,)),
                ((4, 0), ()),
                ((4, 0), (0,)), ((4, 0), (1,)), ((4, 0), (2,)),
                ((4, 1), ()),
                ((4, 1), (0,)), ((4, 1), (1,)), ((4, 1), (2,)),
            ]
        )

    def test_iter_items_start(self):
        result = list(self.model.iter_items((2,)))
        self.assertEqual(
            result,
            [
                ((2,), ()),
                ((2,), (0,)), ((2,), (1,)), ((2,), (2,)),
                ((2, 0), ()),
                ((2, 0), (0,)), ((2, 0), (1,)), ((2, 0), (2,)),
                ((2, 1), ()),
                ((2, 1), (0,)), ((2, 1), (1,)), ((2, 1), (2,)),
            ]
        )

    def test_iter_items_leaf(self):
        result = list(self.model.iter_items((2, 0)))
        self.assertEqual(
            result,
            [
                ((2, 0), ()),
                ((2, 0), (0,)), ((2, 0), (1,)), ((2, 0), (2,)),
            ]
        )
