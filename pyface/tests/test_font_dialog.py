# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from ..font import Font
from ..font_dialog import FontDialog
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

ModalDialogTester = toolkit_object(
    "util.modal_dialog_tester:ModalDialogTester"
)
no_modal_dialog_tester = ModalDialogTester.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestFontDialog(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = FontDialog(font="10pt Arial, Helvetica, sans-serif")

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        del self.dialog
        GuiTestAssistant.tearDown(self)

    def test_font(self):
        # test that creation and destruction works as expected
        self.dialog.font = "10pt Arial"

        self.assertEqual(self.dialog.font, Font.from_description("10pt Arial"))

    def test_create(self):
        # test that creation and destruction works as expected
        with self.event_loop():
            self.dialog._create()
        with self.event_loop():
            self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        with self.event_loop():
            self.dialog.destroy()

    def test_close(self):
        # test that close works
        with self.event_loop():
            self.dialog._create()
        with self.event_loop():
            self.dialog.close()
