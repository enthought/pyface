# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import os
import sys
import unittest

from ..python_shell import PythonShell
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

PYTHON_SCRIPT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "python_shell_script.py")
)


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestPythonShell(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()
        self.window.create()

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
        # test that create/destroy works
        self.widget = PythonShell(self.window.control)

        self.assertIsNone(self.widget.control)

        with self.event_loop():
            self.widget.create(parent=self.window.control)

        self.assertIsNotNone(self.widget.control)

        with self.event_loop():
            self.widget.destroy()

    def test_one_stage_create(self):
        # test that automatic creation works
        with self.event_loop():
            with self.assertWarns(DeprecationWarning):
                self.widget = PythonShell(self.window.control, create=True)

        self.assertIsNotNone(self.widget.control)

        with self.event_loop():
            self.widget.destroy()

    def test_two_stage_create(self):
        # test that create=False works
        with self.assertWarns(DeprecationWarning):
            self.widget = PythonShell(self.window.control, create=False)

        self.assertIsNone(self.widget.control)

        with self.event_loop():
            self.widget.create(parent=self.window.control)

        self.assertIsNotNone(self.widget.control)

        with self.event_loop():
            self.widget.destroy()

    def test_bind(self):
        # test that binding a variable works
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()
        with self.event_loop():
            self.widget.bind("x", 1)

        self.assertEqual(self.widget.interpreter().locals.get("x"), 1)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_command(self):
        # test that executing a command works
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()

        with self.assertTraitChanges(self.widget, "command_executed", count=1):
            with self.event_loop():
                self.widget.execute_command("x = 1")

        self.assertEqual(self.widget.interpreter().locals.get("x"), 1)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_command_not_hidden(self):
        # test that executing a non-hidden command works
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()

        with self.assertTraitChanges(self.widget, "command_executed", count=1):
            with self.event_loop():
                self.widget.execute_command("x = 1", hidden=False)

        self.assertEqual(self.widget.interpreter().locals.get("x"), 1)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_file(self):
        # test that executing a file works
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()

        # XXX inconsistent behaviour between backends
        # with self.assertTraitChanges(self.widget, 'command_executed', count=1):
        with self.event_loop():
            self.widget.execute_file(PYTHON_SCRIPT)

        self.assertEqual(self.widget.interpreter().locals.get("x"), 1)
        self.assertEqual(self.widget.interpreter().locals.get("sys"), sys)

        with self.event_loop():
            self.widget.destroy()

    def test_execute_file_not_hidden(self):
        # test that executing a file works
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()

        # XXX inconsistent behaviour between backends
        # with self.assertTraitChanges(self.widget, 'command_executed', count=1):
        with self.event_loop():
            self.widget.execute_file(PYTHON_SCRIPT, hidden=False)

        self.assertEqual(self.widget.interpreter().locals.get("x"), 1)
        self.assertEqual(self.widget.interpreter().locals.get("sys"), sys)

        with self.event_loop():
            self.widget.destroy()

    def test_get_history(self):
        # test that command history can be extracted
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()

        with self.event_loop():
            self.widget.execute_command("x = 1", hidden=False)

        history, history_index = self.widget.get_history()

        self.assertEqual(history, ["x = 1"])
        self.assertEqual(history_index, 1)

        with self.event_loop():
            self.widget.destroy()

    def test_set_history(self):
        # test that command history can be updated
        self.widget = PythonShell(parent=self.window.control)
        with self.event_loop():
            self.widget.create()

        with self.event_loop():
            self.widget.set_history(["x = 1", "y = x + 1"], 1)

        history, history_index = self.widget.get_history()
        self.assertEqual(history, ["x = 1", "y = x + 1"])
        self.assertEqual(history_index, 1)

        with self.event_loop():
            self.widget.destroy()
