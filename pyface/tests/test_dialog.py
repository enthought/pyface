from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..dialog import Dialog
from ..constant import OK, CANCEL
from ..gui import GUI
from ..toolkit import toolkit_object

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


class TestDialog(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.dialog = Dialog()

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_accept(self):
        # test that accept works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_reject(self):
        # test that reject works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_close(self):
        # test that closing works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_ok(self):
        # test that OK works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_ok())
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        # test that cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.click_cancel())
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_ok(self):
        self.dialog.ok_label = u"Sure"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"Sure"))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_cancel(self):
        self.dialog.cancel_label = u"I Don't Think So"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"I Don't Think So"))
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_help(self):
        def click_help_and_close(tester):
            tester.click_widget(u"Help")
            tester.close(accept=True)

        self.dialog.help_id = "help_test"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=click_help_and_close)
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_help(self):
        def click_help_and_close(tester):
            tester.click_widget(u"Assistance")
            tester.close(accept=True)

        self.dialog.help_id = "help_test"
        self.dialog.help_label = u"Assistance"
        # test that OK works as expected if renames
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=click_help_and_close)
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    def test_nonmodal_close(self):
        # test that closing works as expected
        self.dialog.style = 'nonmodal'
        result = self.dialog.open()
        self.gui.process_events()
        self.dialog.close()
        self.gui.process_events()
        self.assertEqual(result, OK)
        self.assertEqual(self.dialog.return_code, OK)
