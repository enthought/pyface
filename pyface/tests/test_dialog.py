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

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()

    def test_size(self):
        # test that default size works as expected
        self.dialog.size = (100, 100)
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_ok_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.ok_label = u"Sure"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_cancel_renamed(self):
        # test that creation and destruction works as expected with cancel_label
        self.dialog.cancel_label = u"I Don't Think So"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_help(self):
        # test that creation and destruction works as expected with help
        self.dialog.help_id = "test_help"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_help_label(self):
        # test that creation and destruction works as expected with help
        self.dialog.help_id = "test_help"
        self.dialog.help_label = u"Assistance"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

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
        tester.open_and_wait(when_opened=lambda x: x.click_button(OK))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        # test that cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.click_button(CANCEL))
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

    def test_not_resizable(self):
        # test that a resizable dialog can be created
        # XXX use nonmodal for better cross-platform coverage
        self.dialog.style = 'nonmodal'
        self.dialog.resizable = False
        result = self.dialog.open()
        self.gui.process_events()
        self.dialog.close()
        self.gui.process_events()
        self.assertEqual(result, OK)
        self.assertEqual(self.dialog.return_code, OK)
