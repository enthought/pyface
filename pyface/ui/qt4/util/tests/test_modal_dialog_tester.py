# Copyright (c) 2013-2015 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Tests for the tabular editor tester. """
from __future__ import absolute_import

import unittest
from six.moves import cStringIO as StringIO
import platform

from pyface.qt import QtGui
from pyface.api import Dialog, MessageDialog, OK, CANCEL
from pyface.toolkit import toolkit_object
from traits.api import HasStrictTraits

from pyface.ui.qt4.util.testing import silence_output
from pyface.ui.qt4.util.gui_test_assistant import GuiTestAssistant
from pyface.ui.qt4.util.modal_dialog_tester import ModalDialogTester
from pyface.util.testing import skip_if_no_traitsui


is_qt = toolkit_object.toolkit == 'qt4'
if is_qt:
    from pyface.qt import qt_api
is_pyqt5 = (is_qt and qt_api == 'pyqt5')


class MyClass(HasStrictTraits):

    def default_traits_view(self):
        from traitsui.api import CancelButton, OKButton, View

        view = View(
            buttons=[OKButton, CancelButton],
            resizable=False,
            title='My class dialog')
        return view

    def run(self):
        ui = self.edit_traits(kind='livemodal')
        if ui.result:
            return 'accepted'
        else:
            return 'rejected'

    def do_not_show_dialog(self):
        return True


@unittest.skipIf(is_pyqt5, "ModalDialogTester not working on pyqt5. Issue #302")
class TestModalDialogTester(unittest.TestCase, GuiTestAssistant):
    """ Tests for the modal dialog tester. """

    #### Tests ################################################################

    def test_on_message_dialog(self):
        dialog = MessageDialog()
        tester = ModalDialogTester(dialog.open)

        # accept
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertTrue(tester.value_assigned())
        self.assertEqual(tester.result, OK)
        self.assertTrue(tester.dialog_was_opened)

        # reject
        tester.open_and_run(when_opened=lambda x: x.close())
        self.assertTrue(tester.value_assigned())
        self.assertEqual(tester.result, CANCEL)
        self.assertTrue(tester.dialog_was_opened)

    @skip_if_no_traitsui
    def test_on_traitsui_dialog(self):
        my_class = MyClass()
        tester = ModalDialogTester(my_class.run)

        # accept
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertTrue(tester.value_assigned())
        self.assertEqual(tester.result, 'accepted')
        self.assertTrue(tester.dialog_was_opened)

        # reject
        tester.open_and_run(when_opened=lambda x: x.close())
        self.assertTrue(tester.value_assigned())
        self.assertEqual(tester.result, 'rejected')
        self.assertTrue(tester.dialog_was_opened)

    @skip_if_no_traitsui
    def test_dialog_was_not_opened_on_traitsui_dialog(self):
        my_class = MyClass()
        tester = ModalDialogTester(my_class.do_not_show_dialog)

        # it runs okay
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertTrue(tester.value_assigned())
        self.assertEqual(tester.result, True)

        # but no dialog is opened
        self.assertFalse(tester.dialog_was_opened)

    def test_capture_errors_on_failure(self):
        dialog = MessageDialog()
        tester = ModalDialogTester(dialog.open)

        def failure(tester):
            try:
                with tester.capture_error():
                    # this failure will appear in the console and get recorded
                    self.fail()
            finally:
                tester.close()
                self.gui.process_events()

        with self.assertRaises(AssertionError):
            alt_stderr = StringIO
            with silence_output(err=alt_stderr):
                tester.open_and_run(when_opened=failure)
            self.assertIn('raise self.failureException(msg)', alt_stderr)

    def test_capture_errors_on_error(self):
        dialog = MessageDialog()
        tester = ModalDialogTester(dialog.open)

        def raise_error(tester):
            try:
                with tester.capture_error():
                    # this error will appear in the console and get recorded
                    1 / 0
            finally:
                tester.close()
                self.gui.process_events()

        with self.assertRaises(ZeroDivisionError):
            alt_stderr = StringIO
            with silence_output(err=alt_stderr):
                tester.open_and_run(when_opened=raise_error)
            self.assertIn('ZeroDivisionError', alt_stderr)

    @unittest.skip("has_widget code not working as designed. Issue #282.")
    def test_has_widget(self):
        dialog = Dialog()
        tester = ModalDialogTester(dialog.open)

        def check_and_close(tester):
            try:
                with tester.capture_error():
                    self.assertTrue(
                        tester.has_widget('OK', QtGui.QAbstractButton)
                    )
                    self.assertFalse(
                        tester.has_widget(text='I am a virtual button')
                    )
            finally:
                tester.close()

        tester.open_and_run(when_opened=check_and_close)

    @unittest.skip("has_widget code not working as designed. Issue #282.")
    def test_find_widget(self):
        dialog = Dialog()
        tester = ModalDialogTester(dialog.open)

        def check_and_close(tester):
            try:
                with tester.capture_error():
                    widget = tester.find_qt_widget(
                        type_=QtGui.QAbstractButton,
                        test=lambda x: x.text() == 'OK'
                    )
                    self.assertIsInstance(widget, QtGui.QPushButton)
            finally:
                tester.close()

        tester.open_and_run(when_opened=check_and_close)


if __name__ == '__main__':
    unittest.main()
