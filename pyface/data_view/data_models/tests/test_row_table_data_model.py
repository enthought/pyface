# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest

from traits.testing.api import UnittestTools

from pyface.data_view.abstract_data_model import DataViewSetError
from pyface.data_view.abstract_value_type import AbstractValueType
from pyface.data_view.value_types.api import (
    FloatValue, IntValue, TextValue, no_value
)
from pyface.data_view.data_models.data_accessors import AttributeDataAccessor
from pyface.data_view.data_models.row_table_data_model import RowTableDataModel


class DataItem:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class TestRowTableDataModel(UnittestTools, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.data = [
            DataItem(a=i, b=10*i, c=str(i)) for i in range(10)
        ]
        self.model = RowTableDataModel(
            data=self.data,
            row_header_data=AttributeDataAccessor(
                attr='a',
                value_type=IntValue(),
            ),
            column_data=[
                AttributeDataAccessor(
                    attr='b',
                    value_type=IntValue(),
                ),
                AttributeDataAccessor(
                    attr='c',
                    value_type=TextValue(),
                )
            ]
        )
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
        model = RowTableDataModel()
        self.assertEqual(model.get_column_count(), 0)
        self.assertTrue(model.can_have_children(()))
        self.assertEqual(model.get_row_count(()), 0)

    def test_get_column_count(self):
        result = self.model.get_column_count()
        self.assertEqual(result, 2)

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
                    self.assertEqual(result, 10)
                else:
                    self.assertEqual(result, 0)

    def test_get_value(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                result = self.model.get_value(row, column)
                if len(row) == 0 and len(column) == 0:
                    self.assertEqual(result, 'A')
                elif len(row) == 0:
                    attr = self.model.column_data[column[0]].attr
                    self.assertEqual(result, attr.title())
                elif len(column) == 0:
                    self.assertEqual(result, row[-1])
                else:
                    attr = self.model.column_data[column[0]].attr
                    self.assertEqual(
                        result,
                        getattr(self.data[row[0]], attr)
                    )

    def test_set_value(self):
        for row, column in self.model.iter_items():
            with self.subTest(row=row, column=column):
                if len(row) == 0 and len(column) == 0:
                    with self.assertRaises(DataViewSetError):
                        self.model.set_value(row, column, 0)
                elif len(row) == 0:
                    with self.assertRaises(DataViewSetError):
                        self.model.set_value(row, column, 0)
                elif len(column) == 0:
                    value = 6.0 * row[0]
                    with self.assertTraitChanges(self.model, "values_changed"):
                        self.model.set_value(row, column, value)
                    self.assertEqual(self.data[row[0]].a, value)
                    self.assertEqual(
                        self.values_changed_event.new,
                        (row, column, row, column)
                    )
                else:
                    value = 6.0 * row[-1] + 2 * column[0]
                    with self.assertTraitChanges(self.model, "values_changed"):
                        self.model.set_value(row, column, value)
                    attr = self.model.column_data[column[0]].attr
                    self.assertEqual(
                        getattr(self.data[row[0]], attr),
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
                    self.assertIs(
                        result,
                        self.model.row_header_data.title_type,
                    )
                elif len(row) == 0:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(
                        result,
                        self.model.column_data[column[0]].title_type,
                    )
                elif len(column) == 0:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(
                        result,
                        self.model.row_header_data.value_type,
                    )
                else:
                    self.assertIsInstance(result, AbstractValueType)
                    self.assertIs(
                        result,
                        self.model.column_data[column[0]].value_type,
                    )

    def test_data_updated(self):
        with self.assertTraitChanges(self.model, "structure_changed"):
            self.model.data = [
                DataItem(a=i+1, b=20*(i+1), c=str(i)) for i in range(10)
            ]
        self.assertTrue(self.structure_changed_event.new)

    def test_row_header_data_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.row_header_data = AttributeDataAccessor(attr='b')
        self.assertEqual(
            self.values_changed_event.new,
            ((), (), (), ())
        )

    def test_row_header_data_values_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.row_header_data.updated = (self.model.row_header_data, 'value')
        self.assertEqual(
            self.values_changed_event.new,
            ((0,), (), (9,), ())
        )

    def test_row_header_data_title_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.row_header_data.updated = (self.model.row_header_data, 'title')
        self.assertEqual(
            self.values_changed_event.new,
            ((), (), (), ())
        )

    def test_column_data_updated(self):
        with self.assertTraitChanges(self.model, "structure_changed"):
            self.model.column_data = [
                AttributeDataAccessor(
                    attr='c',
                    value_type=TextValue(),
                ),
                AttributeDataAccessor(
                    attr='b',
                    value_type=IntValue(),
                ),
            ]
        self.assertTrue(self.structure_changed_event.new)

    def test_column_data_items_updated(self):
        with self.assertTraitChanges(self.model, "structure_changed"):
            self.model.column_data.pop()
        self.assertTrue(self.structure_changed_event.new)

    def test_column_data_value_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.column_data[0].updated = (self.model.column_data[0], 'value')
        self.assertEqual(
            self.values_changed_event.new,
            ((0,), (0,), (9,), (0,))
        )

    def test_column_data_title_updated(self):
        with self.assertTraitChanges(self.model, "values_changed"):
            self.model.column_data[0].updated = (self.model.column_data[0], 'title')
        self.assertEqual(
            self.values_changed_event.new,
            ((), (0,), (), (0,))
        )
