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

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_update(self):
        # test that accept works as expected
        def update(tester):
            for i in range(101):
                self.dialog.update(i)
                self.gui.process_events()

        self.dialog.min = 0
        self.dialog.max = 100
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=update)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        # test that accept works as expected
        def update(tester):
            for i in range(100):
                self.dialog.update(i)
                self.gui.process_events()
            tester.click_cancel()

        self.dialog.min = 0
        self.dialog.max = 100
        self.can_cancel = True
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=update)
        # XXX no distinction between user close and update close
