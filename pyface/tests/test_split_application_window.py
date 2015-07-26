from __future__ import absolute_import

from traits.testing.unittest_tools import unittest, UnittestTools

from ..gui import GUI
from ..split_application_window import SplitApplicationWindow


class TestSplitApplicationWindow(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.window = SplitApplicationWindow()

    def test_destroy(self):
        # test that destroy works even when no control
        self.window.destroy()

    def test_open_close(self):
        # test that openaing and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_show(self):
        # test that opening and closing works as expected
        self.window._create()
        self.window.show(True)
        self.gui.process_events()
        self.window.show(False)
        self.gui.process_events()
        self.window.destroy()
