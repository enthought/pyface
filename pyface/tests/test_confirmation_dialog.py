from __future__ import absolute_import

import platform

from traits.testing.unittest_tools import unittest

from ..confirmation_dialog import ConfirmationDialog, confirm
from ..constant import YES, NO, OK, CANCEL
from ..image_resource import ImageResource
from ..toolkit import toolkit_object
from ..window import Window

is_qt = toolkit_object.toolkit == 'qt4'
if is_qt:
    from pyface.qt import qt_api

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')

is_pyqt5 = (is_qt and qt_api == 'pyqt5')
is_pyqt4_linux = (is_qt and qt_api == 'pyqt' and platform.system() == 'Linux')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestConfirmationDialog(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = ConfirmationDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        self.dialog = None
        GuiTestAssistant.tearDown(self)

    def test_create(self):
        # test that creation and destruction works as expected
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_destroy(self):
        # test that destroy works even when no control
        self.dialog.destroy()
        self.event_loop()

    def test_size(self):
        # test that size works as expected
        self.dialog.size = (100, 100)
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_position(self):
        # test that position works as expected
        self.dialog.position = (100, 100)
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_parent(self):
        # test that creation and destruction works as expected with a parent
        parent = Window()
        self.dialog.parent = parent.control
        parent._create()
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        parent.destroy()
        self.event_loop()

    def test_create_yes_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.yes_label = u"Sure"
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_no_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.no_label = u"No Way"
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_yes_default(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.default = YES
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_cancel(self):
        # test that creation and destruction works with cancel button
        self.dialog.cancel = True
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_cancel_renamed(self):
        # test that creation and destruction works with cancel button
        self.dialog.cancel = True
        self.dialog.cancel_label = "Back"
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_cancel_default(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.cancel = True
        self.dialog.default = CANCEL
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    def test_create_image(self):
        # test that creation and destruction works with a non-standard image
        self.dialog.image = ImageResource('core')
        self.dialog._create()
        self.event_loop()
        self.dialog.destroy()
        self.event_loop()

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_close(self):
        # test that closing works as expected
        # XXX duplicate of Dialog test, not needed?
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.event_loop()

        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_close_with_cancel(self):
        # test that closing works as expected
        self.dialog.cancel = True
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: self.dialog.close())
        self.event_loop()

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_yes(self):
        # test that Yes works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))
        self.event_loop()

        self.assertEqual(tester.result, YES)
        self.assertEqual(self.dialog.return_code, YES)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_yes(self):
        self.dialog.yes_label = u"Sure"
        # test that Yes works as expected if renamed
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"Sure"))
        self.event_loop()

        self.assertEqual(tester.result, YES)
        self.assertEqual(self.dialog.return_code, YES)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_no(self):
        # test that No works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))
        self.event_loop()

        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_no(self):
        self.dialog.no_label = u"No way"
        # test that No works as expected if renamed
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"No way"))
        self.event_loop()

        self.assertEqual(tester.result, NO)
        self.assertEqual(self.dialog.return_code, NO)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        self.dialog.cancel = True
        # test that Cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))
        self.event_loop()

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel_renamed(self):
        self.dialog.cancel = True
        self.dialog.cancel_label = u"Back"
        # test that Cancel works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_widget(u"Back"))
        self.event_loop()

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
        self.event_loop()

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestConfirm(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_reject(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message", cancel=True))
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))
        self.event_loop()
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_yes(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))
        self.event_loop()
        self.assertEqual(tester.result, YES)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_no(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))
        self.event_loop()
        self.assertEqual(tester.result, NO)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_cancel(self):
        # test that cancel works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message", cancel=True))
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))
        self.event_loop()
        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_title(self):
        # test that title works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message",
                                   title='Title'))
        tester.open_and_run(when_opened=lambda x: x.click_button(NO))
        self.event_loop()
        self.assertEqual(tester.result, NO)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_default_yes(self):
        # test that default works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message", default=YES))
        tester.open_and_run(when_opened=lambda x: x.click_button(YES))
        self.event_loop()
        self.assertEqual(tester.result, YES)

    @unittest.skipIf(is_pyqt5, "Confirmation dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(is_pyqt4_linux, "Confirmation dialog click tests don't work reliably on linux.  Issue #282.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_default_cancel(self):
        # test that default works as expected
        tester = ModalDialogTester(lambda: confirm(None, "message",
                                                   cancel=True, default=YES))
        tester.open_and_run(when_opened=lambda x: x.click_button(CANCEL))
        self.event_loop()
        self.assertEqual(tester.result, CANCEL)
