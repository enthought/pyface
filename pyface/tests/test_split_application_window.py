from __future__ import absolute_import

from traits.testing.unittest_tools import unittest, UnittestTools

from ..gui import GUI
from ..heading_text import HeadingText
from ..split_application_window import SplitApplicationWindow


class TestSplitApplicationWindow(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.window = SplitApplicationWindow()

    def test_destroy(self):
        # test that destroy works even when no control
        self.window.destroy()

    def test_open_close(self):
        # test that opening and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_horizontal_split(self):
        # test that horizontal split works
        self.window.direction = 'horizontal'
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_contents(self):
        # test that contents works
        self.window.lhs = HeadingText
        self.window.rhs = HeadingText
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_ratio(self):
        # test that ratio split works
        self.window.ratio = 0.25
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()
