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

from pyface.data_view.index_manager import (
    IntIndexManager, Root, TupleIndexManager,
)


class IndexManagerMixin:

    def test_root_has_no_parent(self):
        with self.assertRaises(IndexError):
            self.index_manager.get_parent_and_row(Root)

    def test_root_to_sequence(self):
        result = self.index_manager.to_sequence(Root)

        self.assertEqual(result, ())

    def test_root_from_sequence(self):
        result = self.index_manager.from_sequence([])

        self.assertIs(result, Root)

    def test_root_id_round_trip(self):
        root_id = self.index_manager.id(Root)
        result = self.index_manager.from_id(root_id)

        self.assertIs(result, Root)

    def test_simple_sequence_round_trip(self):
        sequence = (5,)
        index = self.index_manager.from_sequence(sequence)
        result = self.index_manager.to_sequence(index)

        self.assertEqual(result, sequence)

    def test_simple_sequence_invalid(self):
        sequence = (-5,)
        with self.assertRaises(IndexError):
            self.index_manager.from_sequence(sequence)

    def test_simple_sequence_to_parent_row(self):
        sequence = (5,)
        index = self.index_manager.from_sequence(sequence)
        result = self.index_manager.get_parent_and_row(index)

        self.assertEqual(result, (Root, 5))

    def test_simple_row_round_trip(self):
        index = self.index_manager.create_index(Root, 5)
        result = self.index_manager.get_parent_and_row(index)

        self.assertEqual(result, (Root, 5))

    def test_simple_row_invalid(self):
        with self.assertRaises(IndexError):
            self.index_manager.create_index(Root, -5)

    def test_simple_row_to_sequence(self):
        index = self.index_manager.create_index(Root, 5)
        result = self.index_manager.to_sequence(index)

        self.assertEqual(result, (5,))

    def test_simple_id_round_trip(self):
        index = self.index_manager.create_index(Root, 5)
        id = self.index_manager.id(index)
        result = self.index_manager.from_id(id)

        self.assertEqual(result, index)


class TestIntIndexManager(IndexManagerMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.index_manager = IntIndexManager()

    def tearDown(self):
        self.index_manager.reset()

    def test_create_index_root(self):
        result = self.index_manager.create_index(Root, 5)
        self.assertEqual(result, 5)

    def test_create_index_leaf(self):
        with self.assertRaises(RuntimeError):
            self.index_manager.create_index(5, 1)

    def test_create_index_negative(self):
        with self.assertRaises(IndexError):
            self.index_manager.create_index(Root, -5)


class TestTupleIndexManager(IndexManagerMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.index_manager = TupleIndexManager()

    def tearDown(self):
        self.index_manager.reset()

    def test_complex_sequence_round_trip(self):
        sequence = (5, 6, 7, 8, 9, 10)
        index = self.index_manager.from_sequence(sequence)
        result = self.index_manager.to_sequence(index)

        self.assertEqual(result, sequence)

    def test_complex_sequence_identical_index(self):
        sequence = (5, 6, 7, 8, 9, 10)
        index_1 = self.index_manager.from_sequence(sequence[:])
        index_2 = self.index_manager.from_sequence(sequence[:])

        self.assertIs(index_1, index_2)

    def test_complex_sequence_to_parent_row(self):
        sequence = (5, 6, 7, 8, 9, 10)
        index = self.index_manager.from_sequence(sequence)

        parent, row = self.index_manager.get_parent_and_row(index)

        self.assertEqual(row, 10)
        self.assertIs(
            parent,
            self.index_manager.from_sequence((5, 6, 7, 8, 9))
        )

    def test_complex_index_round_trip(self):
        sequence = (5, 6, 7, 8, 9, 10)

        parent = Root
        for depth, row in enumerate(sequence):
            with self.subTest(depth=depth):
                index = self.index_manager.create_index(parent, row)
                result = self.index_manager.get_parent_and_row(index)
                self.assertIs(result[0], parent)
                self.assertEqual(result[1], row)
                parent = index

    def test_complex_index_create_index_identical(self):
        sequence = (5, 6, 7, 8, 9, 10)

        parent = Root
        for depth, row in enumerate(sequence):
            with self.subTest(depth=depth):
                index_1 = self.index_manager.create_index(parent, row)
                index_2 = self.index_manager.create_index(parent, row)
                self.assertIs(index_1, index_2)
                parent = index_1

    def test_complex_index_to_sequence(self):
        sequence = (5, 6, 7, 8, 9, 10)
        parent = Root
        for depth, row in enumerate(sequence):
            with self.subTest(depth=depth):
                index = self.index_manager.create_index(parent, row)
                result = self.index_manager.to_sequence(index)
                self.assertEqual(result, sequence[:depth+1])
                parent = index

    def test_complex_index_sequence_round_trip(self):
        parent = Root
        for depth, row in enumerate([5, 6, 7, 8, 9, 10]):
            with self.subTest(depth=depth):
                index = self.index_manager.create_index(parent, row)
                sequence = self.index_manager.to_sequence(index)
                result = self.index_manager.from_sequence(sequence)
                self.assertIs(result, index)
                parent = index

    def test_complex_index_id_round_trip(self):
        sequence = (5, 6, 7, 8, 9, 10)
        parent = Root
        for depth, row in enumerate(sequence):
            with self.subTest(depth=depth):
                index = self.index_manager.create_index(parent, row)
                id = self.index_manager.id(index)
                self.assertIsInstance(id, int)
                result = self.index_manager.from_id(id)
                self.assertIs(result, index)
                parent = index
