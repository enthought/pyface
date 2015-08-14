from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..gui import GUI
from ..heading_text import HeadingText
from ..split_panel import SplitPanel
from ..window import Window


class TestHeadingText(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.window = Window()
        self.window._create()

    def tearDown(self):
        self.widget.destroy()
        self.window.destroy()

    def test_lifecycle(self):
        # test that destroy works
        self.widget = SplitPanel(self.window.control)
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_horizontal(self):
        # test that horizontal split works
        self.widget = SplitPanel(self.window.control, direction='horizontal')
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_ratio(self):
        # test that ratio works
        self.widget = SplitPanel(self.window.control, ratio=0.25)
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_contents(self):
        # test that contents works
        self.widget = SplitPanel(self.window.control, lhs=HeadingText,
                                 rhs=HeadingText)
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()
