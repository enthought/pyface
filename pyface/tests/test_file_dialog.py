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

from ..file_dialog import FileDialog
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

ModalDialogTester = toolkit_object(
    "util.modal_dialog_tester:ModalDialogTester"
)
no_modal_dialog_tester = ModalDialogTester.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestFileDialog(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = FileDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        del self.dialog
        GuiTestAssistant.tearDown(self)

    def test_create_wildcard(self):
        wildcard = FileDialog.create_wildcard("Python", "*.py")
        self.assertTrue(len(wildcard) != 0)

    def test_create_wildcard_multiple(self):
        wildcard = FileDialog.create_wildcard(
            "Python", ["*.py", "*.pyo", "*.pyc", "*.pyd"]
        )
        self.assertTrue(len(wildcard) != 0)

    def test_create(self):
        # test that creation and destruction works as expected
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        with self.event_loop():
            self.dialog.destroy()

    def test_close(self):
        # test that close works
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.close()

    def test_default_path(self):
        # test that default path works
        self.dialog.default_path = os.path.join("images", "core.png")
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.close()

    def test_default_dir_and_file(self):
        # test that default dir and path works
        self.dialog.default_directory = "images"
        self.dialog.default_filename = "core.png"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.close()

    def test_open_files(self):
        # test that open files action works
        self.dialog.action = "open files"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.close()

    def test_save_as(self):
        # test that open files action works
        self.dialog.action = "save as"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.close()

    # XXX would be nice to actually test with an open dialog, but not right now
