# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest


from traits.api import HasTraits, Int
from pyface.action.schema._topological_sort import (
    before_after_sort,
    topological_sort,
)


class TestItem(HasTraits):

    id = Int()
    before = Int()
    after = Int()

    def __init__(self, id, **traits):
        super().__init__(id=id, **traits)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return repr(self.id)


class TopologicalSortTestCase(unittest.TestCase):
    def test_before_after_sort_1(self):
        """ Does the before-after sort work?
        """
        items = [
            TestItem(1),
            TestItem(2),
            TestItem(3, before=2),
            TestItem(4, after=1),
            TestItem(5),
        ]
        actual = before_after_sort(items)
        desired = [
            TestItem(1),
            TestItem(3),
            TestItem(4),
            TestItem(2),
            TestItem(5),
        ]
        self.assertEqual(actual, desired)

    def test_before_after_sort_2(self):
        """ Does the before-after sort work when both 'before' and 'after'
            are set?
        """
        items = [
            TestItem(1),
            TestItem(2),
            TestItem(3),
            TestItem(4, after=2, before=3),
        ]
        actual = before_after_sort(items)
        desired = [TestItem(1), TestItem(2), TestItem(4), TestItem(3)]
        self.assertEqual(actual, desired)

    def test_before_after_sort_3(self):
        """ Does the degenerate case for the before-after sort work?
        """
        actual = before_after_sort([TestItem(1)])
        desired = [TestItem(1)]
        self.assertEqual(actual, desired)

    def test_topological_sort_1(self):
        """ Does a basic topological sort work?
        """
        pairs = [(1, 2), (3, 5), (4, 6), (1, 3), (1, 4), (1, 6), (2, 4)]
        result, has_cycles = topological_sort(pairs)
        self.assertTrue(not has_cycles)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_topological_sort_2(self):
        """ Does another basic topological sort work?
        """
        pairs = [(1, 2), (1, 3), (2, 4), (3, 4), (5, 6), (4, 5)]
        result, has_cycles = topological_sort(pairs)
        self.assertTrue(not has_cycles)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_topological_sort_3(self):
        """ Does cycle detection work?
        """
        pairs = [(1, 2), (2, 3), (3, 1)]
        result, has_cycles = topological_sort(pairs)
        self.assertTrue(has_cycles)
