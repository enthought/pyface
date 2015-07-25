from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..about_dialog import AboutDialog
from ..constant import OK, CANCEL
from ..gui import GUI
from ..toolkit import toolkit_object
from ..window import Window

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


class TestAboutDialog(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.dialog = AboutDialog()

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_accept(self):
        # test that accept works as expected
        # XXX duplicate of Dialog test, not needed?
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_close(self):
        # test that closing works as expected
        # XXX duplicate of Dialog test, not needed?
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_ok(self):
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_ok())
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_ok(self):
        self.dialog.ok_label = u"Sure"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"Sure"))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_parent(self):
        # test that lifecycle works with a parent
        parent = Window()
        self.dialog.parent = parent.control
        parent.open()
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        parent.close()
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)
