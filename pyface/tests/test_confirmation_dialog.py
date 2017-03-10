from __future__ import absolute_import

import os
from qtpy import PYQT5
from traits.testing.unittest_tools import unittest

from ..confirmation_dialog import ConfirmationDialog, confirm
from ..constant import YES, NO, OK, CANCEL
from ..image_resource import ImageResource
from ..toolkit import toolkit_object
from ..window import Window

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')
GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')


@unittest.skipIf(PYQT5, 'avoid Qt5 segfault')
class TestConfirmationDialog(GuiTestAssistant, unittest.TestCase):

    def setUp(self):
        super(TestConfirmationDialog, self).setUp()
        self.dialog = ConfirmationDialog()

    def tearDown(self):
        self.dialog.destroy()
        super(TestConfirmationDialog, self).tearDown()

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()

    def test_size(self):
        # test that size works as expected
        self.dialog.size = (100, 100)
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_position(self):
        # test that position works as expected
        self.dialog.position = (100, 100)
        self.dialog._create()
        self.gui.process_events()
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
        self.dialog.yes_label = "Sure"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_create_no_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.no_label = "No Way"
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
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))
        self.assertEqual(tester.result, YES)
        self.assertEqual(self.dialog.return_code, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_yes(self):
        self.dialog.yes_label = "Sure"
        # test that Yes works as expected if renamed
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget("Sure"))
        self.assertEqual(tester.result, YES)
        self.assertEqual(self.dialog.return_code, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_no(self):
        # test that No works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))
        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_no(self):
        self.dialog.no_label = "No way"
        # test that No works as expected if renamed
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget("No way"))
        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        self.dialog.cancel = True
        # test that Cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))
        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel_renamed(self):
        self.dialog.cancel = True
        self.dialog.cancel_label = "Back"
        # test that Cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget("Back"))
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


@unittest.skipIf(PYQT5, 'avoid Qt5 segfault')
class TestConfirm(GuiTestAssistant, unittest.TestCase):

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_reject(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message", cancel=True))
        tester.open_and_wait(when_opened=lambda x: x.close(accept=False))
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_yes(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))
        self.gui.process_events()
        self.assertEqual(tester.result, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_no(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))
        self.gui.process_events()
        self.assertEqual(tester.result, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message", cancel=True))
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))
        self.gui.process_events()
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_title(self):
        # test that title works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message",
                                   title='Title'))
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))
        self.assertEqual(tester.result, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_default_yes(self):
        # test that default works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message", default=YES))
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))
        self.assertEqual(tester.result, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_default_cancel(self):
        # test that default works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message",
                                                   cancel=True, default=YES))
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))
        self.assertEqual(tester.result, CANCEL)
