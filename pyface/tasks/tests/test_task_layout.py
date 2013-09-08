# Standard library imports.
import unittest

# Enthought library imports.
from pyface.tasks.api import HSplitter, PaneItem, Tabbed, VSplitter


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


if __name__ == '__main__':
    unittest.main()
