from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..constant import CANCEL
from ..gui import GUI
from ..progress_dialog import ProgressDialog
from ..toolkit import toolkit_object

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
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
        self.dialog.can_cancel =  True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_show_time(self):
        # test that creation works with show_time
        self.dialog.show_time =  True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    @unittest.skip("not implemented in any backend")
    def test_show_percent(self):
        # test that creation works with show_percent
        self.dialog.show_percent =  True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_update(self):
        self.dialog.min = 0
        self.dialog.max = 100
        self.dialog.open()
        for i in range(101):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))

    def test_incomplete_update(self):
        self.dialog.min = 0
        self.dialog.max = 100
        self.can_cancel = True
        self.dialog.open()
        for i in range(50):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
        self.dialog.close()

    def test_change_message(self):
        self.dialog.min = 0
        self.dialog.max = 100
        self.dialog.open()
        for i in range(101):
            self.dialog.change_message('Updating {}'.format(i))
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))

    def test_update_show_time(self):
        self.dialog.min = 0
        self.dialog.max = 100
        self.show_time = True
        self.dialog.open()
        for i in range(101):
            result = self.dialog.update(i)
            self.gui.process_events()
            self.assertEqual(result, (True, False))
