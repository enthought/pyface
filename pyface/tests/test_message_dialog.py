from __future__ import absolute_import

from traits.etsconfig.api import ETSConfig
from traits.testing.unittest_tools import unittest

from ..message_dialog import MessageDialog
from ..constant import OK, CANCEL
from ..gui import GUI
from ..toolkit import toolkit_object
from ..window import Window

ModalDialogTester = toolkit_object('util.modal_dialog_tester:ModalDialogTester')
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')

USING_QT = ETSConfig.toolkit not in ['', 'wx']

class TestMessageDialog(unittest.TestCase):

    def setUp(self):
        self.gui = GUI()
        self.dialog = MessageDialog()

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
