from __future__ import absolute_import

import os
import sys
import unittest

from ..python_shell import PythonShell
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

PYTHON_SCRIPT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'python_shell_script.py')
)


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestPythonShell(unittest.TestCase, GuiTestAssistant):
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
            self.widget = PythonShell(self.window.control)
        with self.event_loop():
            self.widget.destroy()

    def test_bind(self):
        # test that binding a variable works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)
        with self.event_loop():
            self.widget.bind('x', 1)

        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_command(self):
        # test that executing a command works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)

        with self.assertTraitChanges(self.widget, 'command_executed', count=1):
            with self.event_loop():
                self.widget.execute_command('x = 1')

        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_command_not_hidden(self):
        # test that executing a non-hidden command works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)

        with self.assertTraitChanges(self.widget, 'command_executed', count=1):
            with self.event_loop():
                self.widget.execute_command('x = 1', hidden=False)

        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_file(self):
        # test that executing a file works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)

        # XXX inconsistent behaviour between backends
        #with self.assertTraitChanges(self.widget, 'command_executed', count=1):
        with self.event_loop():
            self.widget.execute_file(PYTHON_SCRIPT)

        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.assertEqual(self.widget.interpreter().locals.get('sys'), sys)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_file_not_hidden(self):
        # test that executing a file works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)

        # XXX inconsistent behaviour between backends
        #with self.assertTraitChanges(self.widget, 'command_executed', count=1):
        with self.event_loop():
            self.widget.execute_file(PYTHON_SCRIPT, hidden=False)

        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.assertEqual(self.widget.interpreter().locals.get('sys'), sys)

        with self.event_loop():
            self.widget.destroy()

    def test_get_history(self):
        # test that executing a command works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)

        with self.event_loop():
            self.widget.execute_command('x = 1', hidden=False)

        history, history_index = self.widget.get_history()

        self.assertEqual(history, ['x = 1'])
        self.assertEqual(history_index, 1)

        with self.event_loop():
            self.widget.destroy()

    def test_set_history(self):
        # test that executing a command works
        with self.event_loop():
            self.widget = PythonShell(self.window.control)

        with self.event_loop():
            self.widget.set_history(['x = 1', 'y = x + 1'], 1)

        history, history_index = self.widget.get_history()
        self.assertEqual(history, ['x = 1', 'y = x + 1'])
        self.assertEqual(history_index, 1)

        with self.event_loop():
            self.widget.destroy()
