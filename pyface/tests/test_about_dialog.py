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

from ..about_dialog import AboutDialog
from ..constant import OK, CANCEL
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

ModalDialogTester = toolkit_object(
    "util.modal_dialog_tester:ModalDialogTester"
)
no_modal_dialog_tester = ModalDialogTester.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestAboutDialog(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = AboutDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        self.dialog = None
        GuiTestAssistant.tearDown(self)

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

    def test_create_parent(self):
        # test that creation and destruction works as expected with a parent
        parent = Window()
        with self.event_loop():
            parent.create(parent.control)
            self.dialog.create()

        with self.event_loop():
            self.dialog.destroy()
        with self.event_loop():
            parent.destroy()

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_accept(self):
        # test that accept works as expected
        # XXX duplicate of Dialog test, not needed?
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_close(self):
        # test that closing works as expected
        # XXX duplicate of Dialog test, not needed?
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_parent(self):
        # test that lifecycle works with a parent
        parent = Window()
        self.dialog.parent = parent.control
        parent.open()
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        with self.event_loop():
            parent.close()

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    def test__create_html(self):
        # test that the html content is properly created
        self.dialog.additions.extend(["test line 1", "test line 2"])
        self.dialog.copyrights.extend(["copyright", "copyleft"])
        html = self.dialog._create_html()
        self.assertIn("test line 1<br />test line 2<br>", html)
        self.assertIn(
            "Copyright &copy; copyright<br />Copyright &copy; copyleft", html
        )

    def test_image_default(self):
        # test that the default image is found
        import pyface
        expected_path = os.path.join(
            os.path.dirname(pyface.__file__),
            "images",
            "about.png",
        )
        self.assertEqual(
            self.dialog.image.absolute_path,
            expected_path,
        )
