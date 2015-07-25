from __future__ import absolute_import

from traits.testing.unittest_tools import unittest, UnittestTools

from ..constant import CANCEL, NO, OK, YES
from ..gui import GUI
from ..toolkit import toolkit_object
from ..window import Window

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


class TestWindow(unittest.TestCase, UnittestTools):

    def setUp(self):
        self.gui = GUI()
        self.window = Window()

    def test_open_close(self):
        # test that openaing and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                self.window.open()
        self.gui.process_events()
        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                self.window.close()
        self.gui.process_events()

    def test_show(self):
        # test that openaing and closing works as expected
        self.window._create()
        self.window.show(True)
        self.gui.process_events()
        self.window.show(False)
        self.gui.process_events()
        self.window.destroy()

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_confirm_reject(self):
        # test that cancel works as expected
        tester = ModalDialogTester(
            lambda: self.window.confirm("message", cancel=True))
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_confirm_yes(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: self.window.confirm("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_yes())
        self.gui.process_events()
        self.assertEqual(tester.result, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_confirm_no(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: self.window.confirm("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_no())
        self.gui.process_events()
        self.assertEqual(tester.result, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_confirm_cancel(self):
        # test that yes works as expected
        tester = ModalDialogTester(
            lambda: self.window.confirm("message", cancel=True))
        tester.open_and_wait(when_opened=lambda x: x.click_cancel())
        self.gui.process_events()
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_information_accept(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: self.window.information("message"))
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertIsNone(tester.result)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_information_ok(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: self.window.information("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_ok())
        self.assertIsNone(tester.result)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_warning_accept(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: self.window.warning("message"))
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertIsNone(tester.result)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_warning_ok(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: self.window.warning("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_ok())
        self.assertIsNone(tester.result)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_error_accept(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: self.window.error("message"))
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertIsNone(tester.result)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_error_ok(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: self.window.error("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_ok())
        self.assertIsNone(tester.result)
