from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..confirmation_dialog import ConfirmationDialog
from ..constant import YES, NO, OK, CANCEL
from ..gui import GUI
from ..image_resource import ImageResource
from ..toolkit import toolkit_object
from ..window import Window

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')


class TestConfirmationDialog(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.dialog = ConfirmationDialog()

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()

    def test_create_parent(self):
        # test that creation and destruction works as expected with a parent
        parent = Window()
        self.dialog.parent = parent.control
        parent._create()
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()
        parent.destroy()

    def test_create_yes_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.yes_label = u"Sure"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_no_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.no_label = u"No Way"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_yes_default(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.default = YES
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_cancel(self):
        # test that creation and destruction works with cancel button
        self.dialog.cancel = True
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_cancel_renamed(self):
        # test that creation and destruction works with cancel button
        self.dialog.cancel = True
        self.dialog.cancel_label = "Back"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_cancel_default(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.cancel = True
        self.dialog.default = CANCEL
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_image(self):
        # test that creation and destruction works with a non-standard image
        self.dialog.image = ImageResource('core')
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_close(self):
        # test that closing works as expected
        # XXX duplicate of Dialog test, not needed?
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_close_with_cancel(self):
        # test that closing works as expected
        self.dialog.cancel = True
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_yes(self):
        # test that Yes works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_yes())
        self.assertEqual(tester.result, YES)
        self.assertEqual(self.dialog.return_code, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_yes(self):
        self.dialog.yes_label = u"Sure"
        # test that Yes works as expected if renamed
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"Sure"))
        self.assertEqual(tester.result, YES)
        self.assertEqual(self.dialog.return_code, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_no(self):
        # test that No works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_no())
        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_no(self):
        self.dialog.no_label = u"No way"
        # test that No works as expected if renamed
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"No way"))
        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        self.dialog.cancel = True
        # test that Cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_cancel())
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel_renamed(self):
        self.dialog.cancel = True
        self.dialog.cancel_label = u"Back"
        # test that Cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"Back"))
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

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
