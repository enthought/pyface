from __future__ import absolute_import

import os
import sys
import unittest

from ..python_editor import PythonEditor
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

PYTHON_SCRIPT = os.path.join(
    os.path.dirname(__file__), 'python_shell_script.py'
)


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestPythonEditor(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()
        self.window._create()

    def tearDown(self):
        if self.widget.control is not None:
            with self.delete_widget(self.widget.control):
                self.widget.destroy()
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()
        del self.widget
        del self.window
        GuiTestAssistant.tearDown(self)

    def test_lifecycle(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(self.window.control)

        self.assertFalse(self.widget.dirty)

        with self.event_loop():
            self.widget.destroy()

    def test_show_line_numbers(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(
                self.window.control, show_line_numbers=False
            )
        with self.event_loop():
            self.widget.show_line_numbers = True
        with self.event_loop():
            self.widget.show_line_numbers = False
        with self.event_loop():
            self.widget.destroy()

    def test_load(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(self.window.control)

        with self.assertTraitChanges(self.widget, 'changed', count=1):
            with self.event_loop():
                self.widget.path = PYTHON_SCRIPT
        self.assertFalse(self.widget.dirty)

        with self.event_loop():
            self.widget.destroy()

    def test_select_line(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(self.window.control, path=PYTHON_SCRIPT)

        with self.event_loop():
            self.widget.select_line(3)

        with self.event_loop():
            self.widget.destroy()
