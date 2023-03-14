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
import unittest

from ..python_editor import PythonEditor
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

PYTHON_SCRIPT = os.path.join(
    os.path.dirname(__file__), "python_shell_script.py"
)


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestPythonEditor(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()
        self.window.create()

    def tearDown(self):
        if self.widget.control is not None:
            with self.delete_widget(self.window.control):
                self.widget.destroy()
        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()
        del self.widget
        del self.window
        GuiTestAssistant.tearDown(self)

    def test_lifecycle(self):
        # test that create/destroy works
        self.widget = PythonEditor(self.window.control)

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
                self.widget = PythonEditor(self.window.control, create=True)

        self.assertIsNotNone(self.widget.control)

        with self.event_loop():
            self.widget.destroy()

    def test_two_stage_create(self):
        # test that create=False works
        with self.assertWarns(DeprecationWarning):
            self.widget = PythonEditor(self.window.control, create=False)

        self.assertIsNone(self.widget.control)

        with self.event_loop():
            self.widget.create(parent=self.window.control)

        self.assertIsNotNone(self.widget.control)

        with self.event_loop():
            self.widget.destroy()

    def test_show_line_numbers(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(
                parent=self.window.control,
                show_line_numbers=False,
            )
            self.widget.create()

        with self.event_loop():
            self.widget.show_line_numbers = True

        with self.event_loop():
            self.widget.show_line_numbers = False

        with self.event_loop():
            self.widget.destroy()

    def test_load(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(
                parent=self.window.control,
            )
            self.widget.create()

        with self.assertTraitChanges(self.widget, "changed", count=1):
            with self.event_loop():
                self.widget.path = PYTHON_SCRIPT
        self.assertFalse(self.widget.dirty)

        with self.event_loop():
            self.widget.destroy()

    def test_select_line(self):
        # test that destroy works
        with self.event_loop():
            self.widget = PythonEditor(
                parent=self.window.control,
                path=PYTHON_SCRIPT,
            )
            self.widget.create()

        with self.event_loop():
            self.widget.select_line(3)

        with self.event_loop():
            self.widget.destroy()
