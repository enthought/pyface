from __future__ import absolute_import

import unittest

from ..progress_dialog import ProgressDialog
from ..toolkit import toolkit_object

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

ModalDialogTester = toolkit_object(
    'util.modal_dialog_tester:ModalDialogTester'
)
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestProgressDialog(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = ProgressDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        del self.dialog
        GuiTestAssistant.tearDown(self)

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

    def test_can_cancel(self):
        # test that creation works with can_cancel
        self.dialog.can_cancel = True
        with self.event_loop():
            self.dialog._create()
        with self.event_loop():
            self.dialog.destroy()

    def test_show_time(self):
        # test that creation works with show_time
        self.dialog.show_time = True
        with self.event_loop():
            self.dialog._create()
        with self.event_loop():
            self.dialog.destroy()

    @unittest.skip("not implemented in any backend")
    def test_show_percent(self):
        # test that creation works with show_percent
        self.dialog.show_percent = True
        with self.event_loop():
            self.dialog._create()
        with self.event_loop():
            self.dialog.destroy()

    def test_update(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            with self.event_loop():
                result = self.dialog.update(i)

            self.assertEqual(result, (True, False))

        self.assertIsNone(self.dialog.control)

    @unittest.skip("inconsistent implementations")
    def test_update_no_control(self):
        self.dialog.min = 0
        self.dialog.max = 10
        with self.event_loop():
            result = self.dialog.update(1)
        self.assertEqual(result, (None, None))

    def test_incomplete_update(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.can_cancel = True
        self.dialog.open()
        for i in range(5):
            with self.event_loop():
                result = self.dialog.update(i)
            self.assertEqual(result, (True, False))
        self.assertIsNotNone(self.dialog.control)
        with self.event_loop():
            self.dialog.close()

        self.assertIsNone(self.dialog.control)

    def test_change_message(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            with self.event_loop():
                self.dialog.change_message('Updating {}'.format(i))
                result = self.dialog.update(i)

            self.assertEqual(result, (True, False))
            self.assertEqual(self.dialog.message, 'Updating {}'.format(i))
        self.assertIsNone(self.dialog.control)

    def test_update_show_time(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.show_time = True
        self.dialog.open()
        for i in range(11):
            with self.event_loop():
                result = self.dialog.update(i)

            self.assertEqual(result, (True, False))
        self.assertIsNone(self.dialog.control)

    def test_update_degenerate(self):
        self.dialog.min = 0
        self.dialog.max = 0
        self.dialog.open()
        for i in range(10):
            with self.event_loop():
                result = self.dialog.update(i)

            self.assertEqual(result, (True, False))

        with self.event_loop():
            self.dialog.close()
        # XXX not really sure what correct behaviour is here

    def test_update_negative(self):
        self.dialog.min = 0
        self.dialog.max = -10
        with self.assertRaises(AttributeError):
            with self.event_loop():
                self.dialog.open()

        self.assertIsNone(self.dialog.control)
