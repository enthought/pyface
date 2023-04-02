# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from ..color import Color
from ..color_dialog import ColorDialog, get_color
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

ModalDialogTester = toolkit_object(
    "util.modal_dialog_tester:ModalDialogTester"
)
no_modal_dialog_tester = ModalDialogTester.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestColorDialog(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = ColorDialog(color="rebeccapurple")

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        del self.dialog
        GuiTestAssistant.tearDown(self)

    def test_color(self):
        # test that colors are translated as expected
        self.dialog.color = "red"

        self.assertEqual(self.dialog.color, Color.from_str("red"))

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

    def test_show_alpha(self):
        # test that creation and destruction works with show_alpha True
        self.dialog.show_alpha = True

        with self.event_loop():
            self.dialog.create()


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestGetColor(unittest.TestCase, GuiTestAssistant):

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_close(self):
        # test that cancel works as expected
        tester = ModalDialogTester(
            lambda: get_color(None, "rebeccapurple")
        )
        tester.open_and_wait(when_opened=lambda x: x.close(accept=False))

        self.assertEqual(tester.result, None)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_close_show_alpha(self):
        # test that cancel works as expected
        tester = ModalDialogTester(
            lambda: get_color(None, "rebeccapurple", True)
        )
        tester.open_and_wait(when_opened=lambda x: x.close(accept=False))

        self.assertEqual(tester.result, None)
