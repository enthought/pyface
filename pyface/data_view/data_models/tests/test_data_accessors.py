# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from types import MappingProxyType
import unittest

from traits.api import TraitError
from traits.testing.api import UnittestTools

from pyface.data_view.abstract_data_model import DataViewSetError
from pyface.data_view.value_types.api import TextValue
from pyface.data_view.data_models.data_accessors import (
    AttributeDataAccessor,
    ConstantDataAccessor,
    IndexDataAccessor,
    KeyDataAccessor,
)


class AttributeDummy:

    def __init__(self, attr_value):
        self.attr_value = attr_value


class DataAccessorMixin(UnittestTools):

    def accessor_observer(self, event):
        self.accessor_event = event

    def test_title_type_changed(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.title_type = TextValue()

        self.assertEqual(self.accessor_event.new, (accessor, 'title'))

    def test_title_type_updated(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.title_type.updated = True

        self.assertEqual(self.accessor_event.new, (accessor, 'title'))

    def test_value_type_changed(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.value_type = TextValue()

        self.assertEqual(self.accessor_event.new, (accessor, 'value'))

    def test_value_type_updated(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.value_type.updated = True

        self.assertEqual(self.accessor_event.new, (accessor, 'value'))


class TestConstantDataAccessor(unittest.TestCase, DataAccessorMixin):

    def create_accessor(self):
        return ConstantDataAccessor(
            title='Test',
            value='test',
            value_type=TextValue(),
        )

    def test_defaults(self):
        accessor = ConstantDataAccessor()

        self.assertEqual(accessor.value, None)
        self.assertIsNone(accessor.value_type)
        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, '')

    def test_typical_defaults(self):
        accessor = self.create_accessor()

        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, 'Test')

    def test_get_value(self):
        accessor = self.create_accessor()
        obj = object()

        value = accessor.get_value(obj)

        self.assertEqual(value, 'test')

    def test_can_set_value(self):
        accessor = self.create_accessor()
        obj = object()

        can_set = accessor.can_set_value(obj)

        self.assertFalse(can_set)

    def test_set_value_error(self):
        accessor = self.create_accessor()
        obj = object()

        with self.assertRaises(DataViewSetError):
            accessor.set_value(obj, 'new_value')

    def test_value_updated(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.value = 'other_value'

        self.assertEqual(self.accessor_event.new, (accessor, 'value'))


class TestAttributeDataAccessor(unittest.TestCase, DataAccessorMixin):

    def create_accessor(self):
        return AttributeDataAccessor(
            attr='attr_value',
            value_type=TextValue(),
        )

    def test_defaults(self):
        accessor = AttributeDataAccessor()

        self.assertEqual(accessor.attr, '')
        self.assertIsNone(accessor.value_type)
        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, '')

    def test_typical_defaults(self):
        accessor = self.create_accessor()

        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, 'Attr Value')

    def test_get_value(self):
        accessor = self.create_accessor()
        obj = AttributeDummy('test_value')

        value = accessor.get_value(obj)

        self.assertEqual(value, 'test_value')

    def test_get_value_extended(self):
        accessor = self.create_accessor()
        accessor.attr = 'attr_value.attr_value'
        obj = AttributeDummy(AttributeDummy('test_value'))

        value = accessor.get_value(obj)

        self.assertEqual(value, 'test_value')

    def test_get_value_missing(self):
        accessor = self.create_accessor()
        accessor.attr = ''
        obj = AttributeDummy('test_value')

        with self.assertRaises(AttributeError):
            accessor.get_value(obj)

    def test_get_value_error(self):
        accessor = self.create_accessor()
        accessor.attr = 'other_attr'
        obj = AttributeDummy('test_value')

        with self.assertRaises(AttributeError):
            accessor.get_value(obj)

    def test_can_set_value(self):
        accessor = self.create_accessor()
        obj = AttributeDummy('test_value')

        can_set = accessor.can_set_value(obj)

        self.assertTrue(can_set)

    def test_can_set_value_false(self):
        accessor = AttributeDataAccessor()
        obj = AttributeDummy('test_value')

        can_set = accessor.can_set_value(obj)

        self.assertFalse(can_set)

    def test_set_value(self):
        accessor = self.create_accessor()
        obj = AttributeDummy('test_value')

        accessor.set_value(obj, 'new_value')

        self.assertEqual(obj.attr_value, 'new_value')

    def test_set_value_extended(self):
        accessor = self.create_accessor()
        accessor.attr = 'attr_value.attr_value'
        obj = AttributeDummy(AttributeDummy('test_value'))

        accessor.set_value(obj, 'new_value')

        self.assertEqual(obj.attr_value.attr_value, 'new_value')

    def test_set_value_error(self):
        accessor = AttributeDataAccessor()
        obj = AttributeDummy('test_value')

        with self.assertRaises(DataViewSetError):
            accessor.set_value(obj, 'new_value')

    def test_attr_updated(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.attr = 'other_attr'

        self.assertEqual(self.accessor_event.new, (accessor, 'value'))


class TestIndexDataAccessor(unittest.TestCase, DataAccessorMixin):

    def create_accessor(self):
        return IndexDataAccessor(
            index=1,
            value_type=TextValue(),
        )

    def test_defaults(self):
        accessor = IndexDataAccessor()

        self.assertEqual(accessor.index, 0)
        self.assertIsNone(accessor.value_type)
        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, '0')

    def test_typical_defaults(self):
        accessor = self.create_accessor()

        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, '1')

    def test_get_value(self):
        accessor = self.create_accessor()
        obj = ['zero', 'one', 'two', 'three']

        value = accessor.get_value(obj)

        self.assertEqual(value, 'one')

    def test_get_value_out_of_bounds(self):
        accessor = self.create_accessor()
        accessor.index = 10
        obj = ['zero', 'one', 'two', 'three']

        with self.assertRaises(IndexError):
            accessor.get_value(obj)

    def test_can_set_value(self):
        accessor = self.create_accessor()
        obj = ['zero', 'one', 'two', 'three']

        can_set = accessor.can_set_value(obj)

        self.assertTrue(can_set)

    def test_can_set_value_false(self):
        accessor = self.create_accessor()
        obj = ['zero']

        can_set = accessor.can_set_value(obj)

        self.assertFalse(can_set)

    def test_can_set_value_immuatble(self):
        accessor = self.create_accessor()
        obj = ('zero', 'one', 'two', 'three')

        can_set = accessor.can_set_value(obj)

        self.assertFalse(can_set)

    def test_set_value(self):
        accessor = self.create_accessor()
        obj = ['zero', 'one', 'two', 'three']

        accessor.set_value(obj, 'new_value')

        self.assertEqual(obj[1], 'new_value')

    def test_set_value_error(self):
        accessor = self.create_accessor()
        obj = ['zero']

        with self.assertRaises(DataViewSetError):
            accessor.set_value(obj, 'new_value')

    def test_index_updated(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.index = 2

        self.assertEqual(self.accessor_event.new, (accessor, 'value'))


class TestKeyDataAccessor(unittest.TestCase, DataAccessorMixin):

    def create_accessor(self):
        return KeyDataAccessor(
            key='one',
            value_type=TextValue(),
        )

    def test_defaults(self):
        accessor = KeyDataAccessor()

        self.assertIsNone(accessor.key)
        self.assertIsNone(accessor.value_type)
        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, 'None')

    def test_typical_defaults(self):
        accessor = self.create_accessor()

        self.assertIsInstance(accessor.title_type, TextValue)
        self.assertEqual(accessor.title, 'One')

    def test_unhashable_error(self):
        accessor = self.create_accessor()
        with self.assertRaises(TraitError):
            accessor.key = []

    def test_get_value(self):
        accessor = self.create_accessor()
        obj = {'one': 'a', 'two': 'b'}

        value = accessor.get_value(obj)

        self.assertEqual(value, 'a')

    def test_get_value_missing(self):
        accessor = self.create_accessor()
        accessor.key = 'three'
        obj = {'one': 'a', 'two': 'b'}

        with self.assertRaises(KeyError):
            accessor.get_value(obj)

    def test_can_set_value(self):
        accessor = self.create_accessor()
        obj = {'one': 'a', 'two': 'b'}

        can_set = accessor.can_set_value(obj)

        self.assertTrue(can_set)

    def test_can_set_value_new(self):
        accessor = self.create_accessor()
        accessor.key = 'three'
        obj = {'one': 'a', 'two': 'b'}

        can_set = accessor.can_set_value(obj)

        self.assertTrue(can_set)

    def test_can_set_value_immutable(self):
        accessor = self.create_accessor()
        # TODO: eventually replace with frozenmap in 3.9
        obj = MappingProxyType({'one': 'a', 'two': 'b'})

        can_set = accessor.can_set_value(obj)

        self.assertFalse(can_set)

    def test_set_value(self):
        accessor = self.create_accessor()
        obj = {'one': 'a', 'two': 'b'}

        accessor.set_value(obj, 'new_value')

        self.assertEqual(obj['one'], 'new_value')

    def test_set_value_new(self):
        accessor = self.create_accessor()
        accessor.key = 'three'
        obj = {'one': 'a', 'two': 'b'}

        accessor.set_value(obj, 'new_value')

        self.assertEqual(obj['three'], 'new_value')

    def test_set_value_error(self):
        accessor = KeyDataAccessor()
        accessor.key = 'one'
        obj = MappingProxyType({'one': 'a', 'two': 'b'})

        with self.assertRaises(DataViewSetError):
            accessor.set_value(obj, 'new_value')

    def test_key_updated(self):
        accessor = self.create_accessor()
        accessor.observe(self.accessor_observer, 'updated')

        with self.assertTraitChanges(accessor, 'updated', count=1):
            accessor.key = 2

        self.assertEqual(self.accessor_event.new, (accessor, 'value'))
