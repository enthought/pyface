from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..constant import CANCEL
from ..gui import GUI
from ..progress_dialog import ProgressDialog
from ..toolkit import toolkit_object

ModalDialogTester = toolkit_object(
    'util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


class TestDialog(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.dialog = ProgressDialog()

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()

    def test_can_cancel(self):
        # test that creation works with can_cancel
        self.dialog.can_cancel = True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_show_time(self):
        # test that creation works with show_time
        self.dialog.show_time = True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    @unittest.skip("not implemented in any backend")
    def test_show_percent(self):
        # test that creation works with show_percent
        self.dialog.show_percent = True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_update(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
        self.assertIsNone(self.dialog.control)

    @unittest.skip("inconsistent implementations")
    def test_update_no_control(self):
        self.dialog.min = 0
        self.dialog.max = 10
        result = self.dialog.update(1)
        self.assertEqual(result, (None, None))

    def test_incomplete_update(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.can_cancel = True
        self.dialog.open()
        for i in range(5):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
        self.assertIsNotNone(self.dialog.control)
        self.dialog.close()
        self.assertIsNone(self.dialog.control)

    def test_change_message(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.open()
        for i in range(11):
            self.dialog.change_message('Updating {}'.format(i))
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
            self.assertEqual(self.dialog.message, 'Updating {}'.format(i))
        self.assertIsNone(self.dialog.control)

    def test_update_show_time(self):
        self.dialog.min = 0
        self.dialog.max = 10
        self.dialog.show_time = True
        self.dialog.open()
        for i in range(11):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
        self.assertIsNone(self.dialog.control)

    def test_update_degenerate(self):
        self.dialog.min = 0
        self.dialog.max = 0
        self.dialog.open()
        for i in range(10):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
        self.dialog.close()
        # XXX not really sure what correct behaviour is here

    def test_update_negative(self):
        self.dialog.min = 0
        self.dialog.max = -10
        self.dialog.open()
        for i in range(11):
            result = self.dialog.update(1)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
        self.dialog.close()
        self.assertIsNone(self.dialog.control)
