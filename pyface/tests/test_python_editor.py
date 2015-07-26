from __future__ import absolute_import

import os
import sys

from traits.testing.unittest_tools import unittest, UnittestTools

from ..gui import GUI
from ..python_editor import PythonEditor
from ..window import Window


PYTHON_SCRIPT = os.path.join(os.path.dirname(__file__), 'python_shell_script.py')


class TestPythonEditor(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.window = Window()
        self.window._create()

    def tearDown(self):
        self.widget.destroy()
        self.window.destroy()

    def test_lifecycle(self):
        # test that destroy works
        self.widget = PythonEditor(self.window.control)
        self.gui.process_events()
        self.assertFalse(self.widget.dirty)
        self.widget.destroy()
        self.gui.process_events()

    def test_show_line_numbers(self):
        # test that destroy works
        self.widget = PythonEditor(self.window.control, show_line_numbers=False)
        self.gui.process_events()
        self.widget.show_line_numbers = True
        self.gui.process_events()
        self.widget.show_line_numbers = False
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_load(self):
        # test that destroy works
        self.widget = PythonEditor(self.window.control)
        self.gui.process_events()
        with self.assertTraitChanges(self.widget, 'changed', count=1):
            self.widget.path = PYTHON_SCRIPT
        self.assertFalse(self.widget.dirty)
        self.widget.destroy()
        self.gui.process_events()

    def test_select_line(self):
        # test that destroy works
        self.widget = PythonEditor(self.window.control, path=PYTHON_SCRIPT)
        self.gui.process_events()
        self.widget.select_line(3)
        self.widget.destroy()
        self.gui.process_events()
