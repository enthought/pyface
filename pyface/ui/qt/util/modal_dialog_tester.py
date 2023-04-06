# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A class to facilitate testing components that use TraitsUI or Qt Dialogs.

"""
import contextlib
import sys
import traceback

from pyface.api import GUI, OK, CANCEL, YES, NO
from pyface.qt import QtCore, QtGui
from traits.api import Undefined

from .event_loop_helper import EventLoopHelper
from .testing import find_qt_widget


BUTTON_TEXT = {OK: "OK", CANCEL: "Cancel", YES: "Yes", NO: "No"}


class ModalDialogTester(object):
    """ Test helper for code that open a traits ui or QDialog window.

    Notes
    -----
    ::

        # Common usage calling a `function` that will open a dialog and then
        # accept the dialog info.
        tester = ModalDialogTester(function)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertEqual(tester.result, <expected>)

        # Even if the dialog was not opened upon calling `function`,
        # `result` is assigned and the test may not fail.
        # To test if the dialog was once opened:
        self.assertTrue(tester.dialog_was_opened)

    .. note::

       - Proper operation assumes that at all times the dialog is a modal
         window.
       - Errors and failures during the when_opened call do not register with
         the unittest testcases because they take place on a deferred call in
         the event loop. It is advised that the `capture_error` context
         manager is used from the GuiTestAssistant when necessary.

    """

    def __init__(self, function):
        #: The command to call that will cause a dialog to open.
        self.function = function
        self._assigned = False
        self._result = Undefined
        self._qt_app = QtGui.QApplication.instance()
        self._gui = GUI()
        self._event_loop_error = []
        self._helper = EventLoopHelper(qt_app=self._qt_app, gui=self._gui)
        self._dialog_widget = None
        self.dialog_was_opened = False

    @property
    def result(self):
        """ The return value of the provided function.

        """
        return self._result

    @result.setter
    def result(self, value):
        """ Setter methods for the result attribute.

        """
        self._assigned = True
        self._result = value

    def open_and_run(self, when_opened, *args, **kwargs):
        """ Execute the function to open the dialog and run ``when_opened``.

        Parameters
        ----------
        when_opened : Callable
            A callable to be called when the dialog has been created and
            opened. The callable with be called with the tester instance
            as argument.

        *args, **kwargs :
            Additional arguments to be passed to the `function`
            attribute of the tester.

        Raises
        ------
        AssertionError if an assertion error was captured during the
        deferred calls that open and close the dialog.
        RuntimeError if a result value has not been assigned within 15
        seconds after calling `self.function`
        Any other exception that was captured during the deferred calls
        that open and close the dialog.

        .. note:: This method is synchronous

        """
        condition_timer = QtCore.QTimer()

        def handler():
            """ Run the when_opened as soon as the dialog has opened. """
            if self.dialog_opened():
                self._gui.invoke_later(when_opened, self)
                self.dialog_was_opened = True
            else:
                condition_timer.start()

        # Setup and start the timer to fire the handler every 100 msec.
        condition_timer.setInterval(100)
        condition_timer.setSingleShot(True)
        condition_timer.timeout.connect(handler)
        condition_timer.start()

        self._assigned = False
        try:
            # open the dialog on a deferred call.
            self._gui.invoke_later(self.open, *args, **kwargs)
            # wait in the event loop until timeout or a return value assigned.
            self._helper.event_loop_until_condition(
                condition=self.value_assigned, timeout=15
            )
        finally:
            condition_timer.stop()
            condition_timer.timeout.disconnect(handler)
            self._helper.event_loop()
            self.assert_no_errors_collected()

    def open_and_wait(self, when_opened, *args, **kwargs):
        """ Execute the function to open the dialog and wait to be closed.

        Parameters
        ----------
        when_opened : Callable
            A callable to be called when the dialog has been created and
            opened. The callable with be called with the tester instance
            as argument.

        *args, **kwargs :
            Additional arguments to be passed to the `function`
            attribute of the tester.

        Raises
        ------
        AssertionError if an assertion error was captured during the
        deferred calls that open and close the dialog.
        RuntimeError if the dialog has not been closed within 15 seconds after
        calling `self.function`.
        Any other exception that was captured during the deferred calls
        that open and close the dialog.

        .. note:: This method is synchronous

        """
        condition_timer = QtCore.QTimer()

        def handler():
            """ Run the when_opened as soon as the dialog has opened. """
            if self.dialog_opened():
                self._dialog_widget = self.get_dialog_widget()
                self._gui.invoke_later(when_opened, self)
                self.dialog_was_opened = True
            else:
                condition_timer.start()

        def condition():
            if self._dialog_widget is None:
                return False
            else:
                value = self.get_dialog_widget() != self._dialog_widget
                if value:
                    # process any pending events so that we have a clean
                    # event loop before we exit.
                    self._helper.event_loop()
                return value

        # Setup and start the timer to signal the handler every 100 msec.
        condition_timer.setInterval(100)
        condition_timer.setSingleShot(True)
        condition_timer.timeout.connect(handler)
        condition_timer.start()

        self._assigned = False
        try:
            # open the dialog on a deferred call.
            self._gui.invoke_later(self.open, *args, **kwargs)
            # wait in the event loop until timeout or a return value assigned.
            self._helper.event_loop_until_condition(
                condition=condition, timeout=15
            )
        finally:
            condition_timer.stop()
            condition_timer.timeout.disconnect(handler)
            self._dialog_widget = None
            self._helper.event_loop()
            self.assert_no_errors_collected()

    def open(self, *args, **kwargs):
        """ Execute the function that will cause a dialog to be opened.

        Parameters
        ----------
        *args, **kwargs :
            Arguments to be passed to the `function` attribute of the
            tester.

        .. note:: This method is synchronous

        """
        with self.capture_error():
            self.result = self.function(*args, **kwargs)

    def close(self, accept=False):
        """ Close the dialog by accepting or rejecting.

        """
        with self.capture_error():
            widget = self.get_dialog_widget()
            if accept:
                self._gui.invoke_later(widget.accept)
            else:
                self._gui.invoke_later(widget.reject)

    @contextlib.contextmanager
    def capture_error(self):
        """ Capture exceptions, to be used while running inside an event loop.

        When errors and failures take place through an invoke later command
        they might not be caught by the unittest machinery. This context
        manager when used inside a deferred call, will capture the fact that
        an error has occurred and the user can later use the `check for errors`
        command which will raise an error or failure if necessary.

        """
        try:
            yield
        except Exception:
            self._event_loop_error.append(
                (sys.exc_info()[0], traceback.format_exc())
            )

    def assert_no_errors_collected(self):
        """ Assert that the tester has not collected any errors.

        """
        if len(self._event_loop_error) > 0:
            msg = "The following error(s) were detected:\n\n{0}"
            tracebacks = []
            for type_, message in self._event_loop_error:
                if isinstance(type_, AssertionError):
                    msg = "The following failure(s) were detected:\n\n{0}"
                tracebacks.append(message)

            raise type_(msg.format("\n\n".join(tracebacks)))

    def click_widget(self, text, type_=QtGui.QPushButton):
        """ Execute click on the widget of `type_` with `text`.

        This strips '&' chars from the string, since usage varies from platform
        to platform.
        """
        control = self.get_dialog_widget()

        def test(widget):
            # XXX asking for widget.text() causes occasional segfaults on Linux
            # and pyqt (both 4 and 5).  Not sure why this is happening.
            # See issue #282
            return widget.text().replace("&", "") == text

        widget = find_qt_widget(control, type_, test=test)
        if widget is None:
            # this will only occur if there is some problem with the test
            raise RuntimeError("Could not find matching child widget.")
        widget.click()

    def click_button(self, button_id):
        text = BUTTON_TEXT[button_id]
        self.click_widget(text)

    def value_assigned(self):
        """ A value was assigned to the result attribute.

        """
        result = self._assigned
        if result:
            # process any pending events so that we have a clean
            # even loop before we exit.
            self._helper.event_loop()
        return result

    def dialog_opened(self):
        """ Check that the dialog has opened.

        """
        dialog = self.get_dialog_widget()
        if dialog is None:
            return False
        if hasattr(dialog, "_ui"):
            # This is a traitsui dialog, we need one more check.
            ui = dialog._ui
            return ui.info.initialized
        else:
            # This is a simple QDialog.
            return dialog.isVisible()

    def get_dialog_widget(self):
        """ Get a reference to the active modal QDialog widget.

        """
        # It might make sense to also check for active window and active popup
        # window if this Tester is used for non-modal windows.
        return self._qt_app.activeModalWidget()

    def has_widget(self, text=None, type_=QtGui.QPushButton):
        """ Return true if there is a widget of `type_` with `text`.

        """
        if text is None:
            test = None
        else:
            test = lambda qwidget: qwidget.text() == text
        return self.find_qt_widget(type_=type_, test=test) is not None

    def find_qt_widget(self, type_=QtGui.QPushButton, test=None):
        """ Return the widget of `type_` for which `test` returns true.

        """
        if test is None:
            test = lambda x: True
        window = self.get_dialog_widget()
        return find_qt_widget(window, type_, test=test)
