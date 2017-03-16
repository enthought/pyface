from __future__ import absolute_import

import os

from traits.etsconfig.api import ETSConfig
from traits.testing.unittest_tools import unittest

from ..message_dialog import MessageDialog, information, warning, error
from ..constant import OK
from ..gui import GUI
from ..toolkit import toolkit_object
from ..window import Window


GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')

USING_QT = ETSConfig.toolkit not in ['', 'null', 'wx']
is_pyqt5 = (ETSConfig.toolkit == 'qt4' and os.environ.get('QT_API') == 'pyqt5')


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestMessageDialog(unittest.TestCase, GuiTestAssistant):

    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = MessageDialog()

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        GuiTestAssistant.tearDown(self)

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

    def test_create_ok_renamed(self):
        # test that creation and destruction works as expected with ok_label
        self.dialog.ok_label = u"Sure"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_message(self):
        # test that creation and destruction works as expected with message
        self.dialog.message = u"This is the message"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_informative(self):
        # test that creation and destruction works with informative
        self.dialog.message = u"This is the message"
        self.dialog.informative = u"This is the additional message"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_detail(self):
        # test that creation and destruction works with detail
        self.dialog.message = u"This is the message"
        self.dialog.informative = u"This is the additional message"
        self.dialog.detail = u"This is the detail"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_warning(self):
        # test that creation and destruction works with warning message
        self.dialog.severity = "warning"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

    def test_error(self):
        # test that creation and destruction works with error message
        self.dialog.severity = "error"
        self.dialog._create()
        self.gui.process_events()
        self.dialog.destroy()

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
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(is_pyqt5, "Message dialog click tests don't work on pyqt5.")  # noqa
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_ok(self):
        # test that OK works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_wait(when_opened=lambda x: x.click_button(OK))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(USING_QT, "Can't change OK label in Qt")
    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_renamed_ok(self):
        self.dialog.ok_label = u"Sure"
        # test that OK works as expected if renamed
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


@unittest.skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
@unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
class TestMessageDialogHelpers(unittest.TestCase, GuiTestAssistant):

    def test_information(self):
        self._check_dialog(information)

    def test_warning(self):
        self._check_dialog(warning)

    def test_error(self):
        self._check_dialog(error)

    def _check_dialog(self, helper):
        message = 'message'
        kwargs = {
            'title': 'Title',
            'detail': 'Detail',
            'informative': 'Informative'
        }

        # smoke test, since dialog helper is opaque
        result = self._open_and_close(helper, message, **kwargs)

        self.assertIsNone(result)

    def _open_and_close(self, helper, message, **kwargs):
        parent = Window()
        parent.open()

        when_opened = lambda x: x.close(accept=True)

        tester = ModalDialogTester(helper)
        tester.open_and_wait(when_opened, parent.control, message, **kwargs)

        parent.close()
        return tester.result
