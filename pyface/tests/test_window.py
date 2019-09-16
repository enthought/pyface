from __future__ import absolute_import

import os
import platform
import unittest

from pyface.testing.gui_test_case import GuiTestCase
from ..constant import CANCEL, NO, OK, YES
from ..toolkit import toolkit_object
from ..window import Window

is_qt = toolkit_object.toolkit == 'qt4'
if is_qt:
    from pyface.qt import qt_api

ModalDialogTester = toolkit_object(
    'util.modal_dialog_tester:ModalDialogTester'
)
no_modal_dialog_tester = (ModalDialogTester.__name__ == 'Unimplemented')

is_pyqt5 = (is_qt and qt_api == 'pyqt5')
is_pyqt4_linux = (is_qt and qt_api == 'pyqt' and platform.system() == 'Linux')
is_qt_windows = (is_qt and platform.system() == 'Windows')


class TestWindow(GuiTestCase):
    def setUp(self):
        super(TestWindow, self).setUp()
        self.window = Window()

    def tearDown(self):
        self.destroy_widget(self.window)
        del self.window

        super(TestWindow, self).tearDown()

    def test_destroy(self):
        # test that destroy works
        self.window.open()
        control = self.window.control
        self.event_loop_until_condition(lambda: self.window.visible)

        self.window.destroy()
        self.assertIsNone(self.window.control)
        self.assertToolkitControlDestroyedInGui(control)

    def test_destroy_no_control(self):
        # test that destroy works even when no control
        self.window.destroy()
        self.assertIsNone(self.window.control)

    def test_open_close(self):
        # test that opening and closing works as expected
        with self.assertTraitChanges(self.window, 'opening', count=1):
            with self.assertTraitChanges(self.window, 'opened', count=1):
                result = self.window.open()

        self.assertTrue(result)

        control = self.window.control
        self.assertIsNotNone(control)
        self.assertTraitValueInGui(self.window, 'visible', True)

        with self.assertTraitChanges(self.window, 'closing', count=1):
            with self.assertTraitChanges(self.window, 'closed', count=1):
                result = self.window.close()

        self.assertTrue(result)
        self.assertToolkitControlDestroyedInGui(control)

    def test_show(self):
        # test that showing works as expected
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.gui.invoke_later(self.window.show, False)
        self.assertTraitsChangeInGui(self.window, 'visible')
        self.assertFalse(self.window.visible)

        self.gui.invoke_later(self.window.show, True)
        self.assertTraitsChangeInGui(self.window, 'visible')
        self.assertTrue(self.window.visible)

    @unittest.skipIf(not os.environ.get('PYFACE_PATCH_ACTIVATE', False), "Activate is patched.")
    def test_activate(self):
        # test that activation works as expected
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        other_window = Window()
        other_window.open()
        try:
            self.event_loop_until_trait_value(other_window, 'visible', True)

            self.gui.invoke_later(self.window.activate)
            self.assertTraitsChangeInGui(self.window, 'activated')

            self.gui.invoke_later(self.window.activate, False)
            self.assertTraitsChangeInGui(self.window, 'deactivated')
        finally:
            self.destroy_widget(other_window)

    @unittest.skipIf(not os.environ.get('PYFACE_PATCH_ACTIVATE', False), "Activate is patched.")
    def test_activate_no_raise(self):
        # test that activation works as expected
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        other_window = Window()
        other_window.open()
        try:
            self.event_loop_until_trait_value(other_window, 'visible', True)

            self.gui.invoke_later(self.window.activate, False)
            self.assertTraitsChangeInGui(self.window, 'activated')
        finally:
            self.destroy_widget(other_window)

    def test_position(self):
        # test that default position works as expected
        self.window.position = (100, 100)

        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.assertEqual(self.window.position, (100, 100))

    def test_reposition(self):
        # test that changing position works as expected
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.window.position = (100, 100)

        self.assertTraitValueInGui(self.window, "position", (100, 100))

    @unittest.skipIf(is_qt_windows, "Sizing problematic on qt and windows")
    def test_size(self):
        # test that default size works as expected
        self.window.size = (100, 100)

        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.assertEqual(self.window.size, (100, 100))

    def test_resize(self):
        # test that changing size works as expected
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.set_trait_in_event_loop(self.window, 'size', (100, 100))

        self.assertEqual(self.window.size, (100, 100))

    def test_title(self):
        # test that default title works as expected
        self.window.title = "Test Title"

        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.assertEqual(self.window.title, "Test Title")

    def test_retitle(self):
        # test that changing title works as expected
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.set_trait_in_event_loop(self.window, 'title', "Test Title")

        self.assertEqual(self.window.title, "Test Title")

    def test_show_event(self):
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)
        self.window.show(False)
        self.event_loop_until_trait_value(self.window, 'visible', False)

        self.gui.invoke_later(self.window.show, True)

        self.assertTraitsChangeInGui(self.window, 'visible')
        self.assertTrue(self.window.visible)

    def test_hide_event(self):
        self.window.open()
        self.event_loop_until_trait_value(self.window, 'visible', True)

        self.gui.invoke_later(self.window.show, False)

        self.assertTraitsChangeInGui(self.window, 'visible')
        self.assertFalse(self.window.visible)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Confirmation dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Confirmation dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_confirm_reject(self):
        # test that cancel works as expected
        tester = ModalDialogTester(
            lambda: self.window.confirm("message", cancel=True)
        )
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))

        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Confirmation dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Confirmation dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_confirm_yes(self):
        # test that yes works as expected
        tester = ModalDialogTester(lambda: self.window.confirm("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(YES))

        self.assertEqual(tester.result, YES)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Confirmation dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Confirmation dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_confirm_no(self):
        # test that no works as expected
        tester = ModalDialogTester(lambda: self.window.confirm("message"))
        tester.open_and_wait(when_opened=lambda x: x.click_button(NO))

        self.assertEqual(tester.result, NO)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Confirmation dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Confirmation dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_confirm_cancel(self):
        # test that cncel works as expected
        tester = ModalDialogTester(
            lambda: self.window.confirm("message", cancel=True)
        )
        tester.open_and_wait(when_opened=lambda x: x.click_button(CANCEL))

        self.assertEqual(tester.result, CANCEL)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_information_accept(self):
        self._check_message_dialog_accept(self.window.information)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Message dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Message dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_information_ok(self):
        self._check_message_dialog_ok(self.window.information)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_warning_accept(self):
        self._check_message_dialog_accept(self.window.warning)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Message dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Message dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_warning_ok(self):
        self._check_message_dialog_ok(self.window.warning)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    def test_error_accept(self):
        self._check_message_dialog_accept(self.window.error)

    @unittest.skipIf(no_modal_dialog_tester, 'ModalDialogTester unavailable')
    @unittest.skipIf(
        is_pyqt5, "Message dialog click tests don't work on pyqt5."
    )
    @unittest.skipIf(
        is_pyqt4_linux,
        "Message dialog click tests don't work reliably on linux.  Issue #282."
    )
    def test_error_ok(self):
        self._check_message_dialog_ok(self.window.error)

    def _check_message_dialog_ok(self, method):
        tester = self._setup_tester(method)
        tester.open_and_wait(when_opened=lambda x: x.click_button(OK))

        self.assertIsNone(tester.result)

    def _check_message_dialog_accept(self, method):
        tester = self._setup_tester(method)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))

        self.assertIsNone(tester.result)

    def _setup_tester(self, method):
        kwargs = {
            'title': 'Title',
            'detail': 'Detail',
            'informative': 'Informative'
        }
        tester = ModalDialogTester(lambda: method("message", **kwargs))
        return tester
