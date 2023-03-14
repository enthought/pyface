# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import platform
import unittest

from ..dialog import Dialog
from ..constant import OK, CANCEL
from ..toolkit import toolkit_object

is_qt = toolkit_object.toolkit.startswith("qt")
if is_qt:
    from pyface.qt import qt_api

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

ModalDialogTester = toolkit_object(
    "util.modal_dialog_tester:ModalDialogTester"
)
no_modal_dialog_tester = ModalDialogTester.__name__ == "Unimplemented"

is_pyqt5 = is_qt and qt_api == "pyqt5"
is_pyqt4_linux = is_qt and qt_api == "pyqt" and platform.system() == "Linux"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestDialog(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = Dialog()

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

    def test_size(self):
        # test that size works as expected
        self.dialog.size = (100, 100)
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_position(self):
        # test that position works as expected
        self.dialog.position = (100, 100)
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_create_ok_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.ok_label = "Sure"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_create_cancel_renamed(self):
        # test that creation and destruction works as expected with cancel_label
        self.dialog.cancel_label = "I Don't Think So"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_create_help(self):
        # test that creation and destruction works as expected with help
        self.dialog.help_id = "test_help"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_create_help_label(self):
        # test that creation and destruction works as expected with help
        self.dialog.help_id = "test_help"
        self.dialog.help_label = "Assistance"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_accept(self):
        # test that accept works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_reject(self):
        # test that reject works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_close(self):
        # test that closing works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(
        is_pyqt5, "Dialog click tests don't work on pyqt5."
    )  # noqa
    @unittest.skipIf(
        is_pyqt4_linux,
        "Dialog click tests don't work reliably on linux.  Issue #282.",
    )  # noqa
    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_ok(self):
        # test that OK works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(OK))

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(
        is_pyqt5, "Dialog click tests don't work on pyqt5."
    )  # noqa
    @unittest.skipIf(
        is_pyqt4_linux,
        "Dialog click tests don't work reliably on linux.  Issue #282.",
    )  # noqa
    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_cancel(self):
        # test that cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.click_button(CANCEL))

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(
        is_pyqt5, "Dialog click tests don't work on pyqt5."
    )  # noqa
    @unittest.skipIf(
        is_pyqt4_linux,
        "Dialog click tests don't work reliably on linux.  Issue #282.",
    )  # noqa
    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_renamed_ok(self):
        self.dialog.ok_label = "Sure"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget("Sure"))

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(
        is_pyqt5, "Dialog click tests don't work on pyqt5."
    )  # noqa
    @unittest.skipIf(
        is_pyqt4_linux,
        "Dialog click tests don't work reliably on linux.  Issue #282.",
    )  # noqa
    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_renamed_cancel(self):
        self.dialog.cancel_label = "I Don't Think So"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(
            when_opened=lambda x: x.click_widget("I Don't Think So")
        )

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(
        is_pyqt5, "Dialog click tests don't work on pyqt5."
    )  # noqa
    @unittest.skipIf(
        is_pyqt4_linux,
        "Dialog click tests don't work reliably on linux.  Issue #282.",
    )  # noqa
    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_help(self):
        def click_help_and_close(tester):
            tester.click_widget("Help")
            tester.close(accept=True)

        self.dialog.help_id = "help_test"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=click_help_and_close)

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(
        is_pyqt5, "Dialog click tests don't work on pyqt5."
    )  # noqa
    @unittest.skipIf(
        is_pyqt4_linux,
        "Dialog click tests don't work reliably on linux.  Issue #282.",
    )  # noqa
    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_renamed_help(self):
        def click_help_and_close(tester):
            tester.click_widget("Assistance")
            tester.close(accept=True)

        self.dialog.help_id = "help_test"
        self.dialog.help_label = "Assistance"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=click_help_and_close)

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    def test_nonmodal_close(self):
        # test that closing works as expected
        self.dialog.style = "nonmodal"
        result = self.dialog.open()

        with self.event_loop():
            self.dialog.close()

        self.assertEqual(result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    def test_not_resizable(self):
        # test that a resizable dialog can be created
        # XXX use nonmodal for better cross-platform coverage
        self.dialog.style = "nonmodal"
        self.dialog.resizable = False
        with self.event_loop():
            result = self.dialog.open()
        with self.event_loop():
            self.dialog.close()

        self.assertEqual(result, OK)
        self.assertEqual(self.dialog.return_code, OK)
