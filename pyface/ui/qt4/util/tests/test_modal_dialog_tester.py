# Copyright (c) 2013-2015 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Tests for the tabular editor tester. """

import unittest
import cStringIO

from pyface.qt import QtGui
from pyface.api import MessageDialog, OK, CANCEL
from traits.api import HasStrictTraits
from traitsui.api import CancelButton, OKButton, View

from pyface.ui.qt4.util.testing import silence_output
from pyface.ui.qt4.util.gui_test_assistant import GuiTestAssistant
from pyface.ui.qt4.util.modal_dialog_tester import ModalDialogTester


class MyClass(HasStrictTraits):

    def default_traits_view(self):
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

        with self.assertRaises(AssertionError):
            alt_stderr = cStringIO.StringIO
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

        with self.assertRaises(ZeroDivisionError):
            alt_stderr = cStringIO.StringIO
            with silence_output(err=alt_stderr):
                tester.open_and_run(when_opened=raise_error)
            self.assertIn('ZeroDivisionError', alt_stderr)

    def test_has_widget(self):
        my_class = MyClass()
        tester = ModalDialogTester(my_class.run)

        def check_and_close(tester):
            try:
                with tester.capture_error():
                    self.assertTrue(
                        tester.has_widget('OK', QtGui.QPushButton)
                    )
                    self.assertFalse(
                        tester.has_widget(text='I am a virtual button')
                    )
            finally:
                tester.close()

        tester.open_and_run(when_opened=check_and_close)

    def test_find_widget(self):
        my_class = MyClass()
        tester = ModalDialogTester(my_class.run)

        def check_and_close(tester):
            try:
                with tester.capture_error():
                    widget = tester.find_qt_widget(
                        type_=QtGui.QPushButton,
                        test=lambda x: x.text() == 'OK'
                    )
                    self.assertIsInstance(widget, QtGui.QPushButton)
            finally:
                tester.close()

        tester.open_and_run(when_opened=check_and_close)

    def test_dialog_was_not_opened_on_traitsui_dialog(self):
        my_class = MyClass()
        tester = ModalDialogTester(my_class.do_not_show_dialog)

        # it runs okay
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertTrue(tester.value_assigned())
        self.assertEqual(tester.result, True)

        # but no dialog is opened
        self.assertFalse(tester.dialog_was_opened)


if __name__ == '__main__':
    unittest.main()
