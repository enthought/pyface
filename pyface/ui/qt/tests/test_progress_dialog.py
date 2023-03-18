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

from ..progress_dialog import ProgressDialog
from ..util.gui_test_assistant import GuiTestAssistant


class TestProgressDialog(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = ProgressDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        GuiTestAssistant.tearDown(self)

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog.create()
        self.gui.process_events()
        self.assertIsNotNone(self.dialog.control)
        self.assertIsNotNone(self.dialog.progress_bar)
        self.assertIsNotNone(self.dialog._message_control)
        self.assertIsNone(self.dialog._elapsed_control)
        self.assertIsNone(self.dialog._estimated_control)
        self.assertIsNone(self.dialog._remaining_control)
        self.dialog.destroy()
        self.gui.process_events()

    def test_show_time(self):
        # test that creation works with show_time
        self.dialog.show_time = True
        self.dialog.create()
        self.gui.process_events()
        self.assertIsNotNone(self.dialog._elapsed_control)
        self.assertIsNotNone(self.dialog._estimated_control)
        self.assertIsNotNone(self.dialog._remaining_control)
        self.dialog.destroy()
        self.gui.process_events()

    def test_show_percent(self):
        # test that creation works with show_percent
        self.dialog.show_percent = True
        self.dialog.create()
        self.gui.process_events()
        self.assertEqual(self.dialog.progress_bar.format(), "%p%")
        self.dialog.destroy()
        self.gui.process_events()

    def test_update(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
            if i < 10:
                self.assertEqual(self.dialog.progress_bar.value(), i)
        self.assertIsNone(self.dialog.control)
        self.gui.process_events()

    def test_update_no_control(self):
        # note: inconsistent implementation with Wx
        self.dialog.min = 0
        self.dialog.max = 10
        result = self.dialog.update(1)
        self.assertEqual(result, (None, None))
        self.gui.process_events()

    def test_change_message(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            self.dialog.change_message("Updating {}".format(i))
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
            self.assertEqual(self.dialog.message, "Updating {}".format(i))
            self.assertEqual(
                self.dialog._message_control.text(), "Updating {}".format(i)
            )
        self.assertIsNone(self.dialog.control)
        self.gui.process_events()

    def test_change_message_trait(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            self.dialog.message = "Updating {}".format(i)
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
            self.assertEqual(self.dialog.message, "Updating {}".format(i))
            self.assertEqual(
                self.dialog._message_control.text(), "Updating {}".format(i)
            )
        self.assertIsNone(self.dialog.control)
        self.gui.process_events()

    def test_update_show_time(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.show_time = True
        self.dialog.open()
        for i in range(11):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
            self.assertNotEqual(self.dialog._elapsed_control.text(), "")
            self.assertNotEqual(self.dialog._estimated_control.text(), "")
            self.assertNotEqual(self.dialog._remaining_control.text(), "")
        self.assertIsNone(self.dialog.control)
        self.gui.process_events()
