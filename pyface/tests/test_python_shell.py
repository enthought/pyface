from __future__ import absolute_import

import os
import sys

from traits.testing.unittest_tools import unittest

from ..python_shell import PythonShell
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


PYTHON_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                'python_shell_script.py'))


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
        GuiTestAssistant.tearDown(self)

    def test_lifecycle(self):
        # test that destroy works
        self.widget = PythonShell(self.window.control)
        self.gui.process_events()
        self.widget.destroy()
        self.gui.process_events()

    def test_bind(self):
        # test that binding a variable works
        self.widget = PythonShell(self.window.control)
        self.gui.process_events()
        self.widget.bind('x', 1)
        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.widget.destroy()
        self.gui.process_events()

    def test_execute_command(self):
        # test that executing a command works
        self.widget = PythonShell(self.window.control)
        self.gui.process_events()
        with self.assertTraitChanges(self.widget, 'command_executed', count=1):
            self.widget.execute_command('x = 1')
            self.gui.process_events()
        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.widget.destroy()
        self.gui.process_events()

    def test_execute_command_not_hidden(self):
        # test that executing a non-hidden command works
        self.widget = PythonShell(self.window.control)
        self.gui.process_events()
        with self.assertTraitChanges(self.widget, 'command_executed', count=1):
            self.widget.execute_command('x = 1', hidden=False)
            self.gui.process_events()
        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.widget.destroy()
        self.gui.process_events()

    def test_execute_file(self):
        # test that executing a file works
        self.widget = PythonShell(self.window.control)
        self.gui.process_events()
        # XXX inconsistent behaviour between backends
        #with self.assertTraitChanges(self.widget, 'command_executed', count=1):
        self.widget.execute_file(PYTHON_SCRIPT)
        self.gui.process_events()
        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.assertEqual(self.widget.interpreter().locals.get('sys'), sys)
        self.widget.destroy()
        self.gui.process_events()

    def test_execute_file_not_hidden(self):
        # test that executing a file works
        self.widget = PythonShell(self.window.control)
        self.gui.process_events()
        # XXX inconsistent behaviour between backends
        #with self.assertTraitChanges(self.widget, 'command_executed', count=1):
        self.widget.execute_file(PYTHON_SCRIPT, hidden=False)
        self.gui.process_events()
        self.assertEqual(self.widget.interpreter().locals.get('x'), 1)
        self.assertEqual(self.widget.interpreter().locals.get('sys'), sys)
        self.widget.destroy()
        self.gui.process_events()
