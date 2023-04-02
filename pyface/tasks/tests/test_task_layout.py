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


from pyface.tasks.api import HSplitter, PaneItem, Tabbed, VSplitter
from ..task_layout import LayoutContainer


class LayoutItemsTestCase(unittest.TestCase):
    """ Testing that the layout types play nice with each other.

    This is a regression test for issue #87
    (https://github.com/enthought/pyface/issues/87)

    """

    def setUp(self):
        self.items = [HSplitter(), PaneItem(), Tabbed(), VSplitter()]

    def test_hsplitter_items(self):
        layout = HSplitter(*self.items)
        self.assertEqual(layout.items, self.items)

    def test_tabbed_items(self):
        # Tabbed items only accept PaneItems
        items = [PaneItem(), PaneItem()]
        layout = Tabbed(*items)
        self.assertEqual(layout.items, items)

    def test_vsplitter_items(self):
        layout = VSplitter(*self.items)
        self.assertEqual(layout.items, self.items)

    def test_layout_container_positional_items(self):
        items = self.items
        container = LayoutContainer(*items)
        self.assertListEqual(items, container.items)

    def test_layout_container_keyword_items(self):
        items = self.items
        container = LayoutContainer(items=items)
        self.assertListEqual(items, container.items)

    def test_layout_container_keyword_and_positional_items(self):
        items = self.items
        with self.assertRaises(ValueError):
            LayoutContainer(*items, items=items)
