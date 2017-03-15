# (C) Copyright 2014 Enthought, Inc., Austin, TX
# All right reserved.
""" A class to facilitate testing components that use TraitsUI or Wx Dialogs.

"""
import contextlib
import sys
import traceback
from threading import Timer, Thread, Event

import wx

from pyface.api import OK, CANCEL, YES, NO
from pyface.util.guisupport import get_app_wx
from traits.api import Undefined

from .event_loop_helper import EventLoopHelper
from .gui_test_assistant import find_widget
from .helpers import wait_until


is_win32 = (sys.platform == 'win32')
if is_win32:
    from win32gui import (
        EndDialog, EnumWindows, GetActiveWindow, IsWindowEnabled,
        IsWindowVisible)
    from win32process import GetWindowThreadProcessId


BUTTON_TEXT = {
    OK: 'OK',
    CANCEL: 'Cancel',
    YES: '&Yes',
    NO: '&No',
}


class Dummy(wx.Frame):

    def __init__(self, function, *args, **kwargs):
        wx.Frame.__init__(self, None, wx.ID_ANY, "ModalDialogTester")
        wx.CallAfter(function, *args, **kwargs)


class ModalDialogTester(object):
    """ Test helper for code that open a traits ui or QDialog window.

    Usage
    -----
    ::

        # Common usage calling a `function` that will open a dialog and then
        # accept the dialog info.
        tester = ModalDialogTester(function)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertEqual(tester.result, <expected>)


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
        self._gui_app = get_app_wx()
        self._event_loop_error = []
        self._helper = EventLoopHelper(gui_app=self._gui_app)
        self._gui = self._helper.gui
        self._dialog_widget = None
        self._handler = wx.EvtHandler()

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
        when_opened : callable
            A callable to be called when the dialog has been created and
            opened. The callable with be called with the tester instance
            as argument.

        *args, **kwargs :
            Additional arguments to be passed to the `function`
            attribute of the tester.

        Raises
        ------
        AssertionError :
            if an assertion error was captured during the
            deferred calls that open and close the dialog.
        RuntimeError :
            if a result value has not been assigned within 15
            seconds after calling `self.function`
            Any other exception that was captured during the deferred calls
            that open and close the dialog.

        .. note:: This method is synchronous

        """
        condition_timer = wx.Timer(self._handler)

        def handler():
            """ Run the when_opened as soon as the dialog has opened. """
            if self.dialog_opened():
                wx.CallAfter(when_opened, self)
            else:
                condition_timer.Start(100, True)

        # Setup and start the timer to signal the handler every 100 msec.
        self._handler.Bind(
            wx.EVT_TIMER, lambda event: handler(), condition_timer)
        condition_timer.Start(100, True)

        self._assigned = False
        try:
            self._helper.event_loop_until_condition(
                condition=self.value_assigned,
                start=lambda: self.open(*args, **kwargs),
                timeout=5)
        finally:
            condition_timer.Stop()
            self.assert_no_errors_collected()

    def open_and_wait(self, when_opened, *args, **kwargs):
        """ Execute the function to open the dialog and wait to be closed.

        Parameters
        ----------
        when_opened : callable
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
        condition_timer = wx.Timer(self._handler)

        def handler():
            """ Run the when_opened as soon as the dialog has opened. """
            if self.dialog_opened():
                wx.CallAfter(when_opened, self)
            else:
                condition_timer.Start(100, True)

        def condition():
            if self._dialog_widget is None:
                return False
            else:
                return self.get_dialog_widget() != self._dialog_widget

        # Setup and start the timer to signal the handler every 100 msec.
        self._handler.Bind(
            wx.EVT_TIMER, lambda event: handler(), condition_timer)
        condition_timer.Start(100, True)

        self._assigned = False
        try:
            self._helper.event_loop_until_condition(
                condition=condition,
                start=lambda: self.open(*args, **kwargs),
                timeout=5)
        finally:
            condition_timer.Stop()
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
        def close_dialog(dialog, accept):
            if is_win32 and isinstance(dialog, long):
                if accept:
                    self._gui.invoke_later(EndDialog, dialog, 1)
                else:
                    self._gui.invoke_later(EndDialog, dialog, 2)
            else:
                if accept:
                    button = self.find_widget(
                        test=lambda x: x.GetLabelText() == BUTTON_TEXT[OK])
                else:
                    button = self.find_widget(
                        test=lambda x: x.GetLabelText() == BUTTON_TEXT[CANCEL])
                if button is not None:
                    click_event = wx.CommandEvent(
                        wx.wxEVT_COMMAND_BUTTON_CLICKED,
                        button.GetId())
                    button.ProcessEvent(click_event)
                else:
                    if accept:
                        dialog.EndModal(0)
                    else:
                        dialog.EndModal(1)
                self._gui.invoke_later(dialog.Close)
                self._gui.invoke_later(dialog.Destroy)

        with self.capture_error():
            widget = self.get_dialog_widget()
            self._gui.invoke_later(close_dialog, widget, accept)
            wx.Yield()

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
                (sys.exc_info()[0], traceback.format_exc()))
            raise

    def assert_no_errors_collected(self):
        """ Assert that the tester has not collected any errors.

        """
        if len(self._event_loop_error) > 0:
            msg = 'The following error(s) were detected:\n\n{0}'
            tracebacks = []
            for type_, message in self._event_loop_error:
                if isinstance(type_, AssertionError):
                    msg = 'The following failure(s) were detected:\n\n{0}'
                tracebacks.append(message)

            raise type_(msg.format('\n\n'.join(tracebacks)))

    def click_widget(self, text, type_=wx.Button):
        """ Execute click on the widget of `type_` with `text`.

        """
        control = self.get_dialog_widget()
        widget = find_widget(
            control,
            type_,
            test=lambda widget: widget.GetText() == text)
        widget.click()

    def click_button(self, button_id):
        text = BUTTON_TEXT[button_id]
        self.click_widget(text)

    def value_assigned(self):
        """ A value was assigned to the result attribute.

        """
        return self._assigned

    def dialog_opened(self):
        """ Check that the dialog has opened.

        """
        dialog = self.get_dialog_widget()
        if dialog is None:
            opened = False
        elif is_win32 and isinstance(dialog, long):
            # We have a windows handle.
            opened = IsWindowVisible(dialog) and IsWindowEnabled(dialog)
        else:
            # This is a simple wx.Dialog.
            opened = dialog.IsShown()
        return opened

    def get_dialog_widget(self):
        """ Get a reference to the active window widget.

        """
        import os

        window = self._gui_app.GetTopWindow()
        if window is not None and window.GetTitle() != "ModalDialogTester":
            return window
        elif is_win32:
            # Native dialogs do not appear in the wx lists
            handles = []

            def callback(hwnd, extra):
                info = GetWindowThreadProcessId(hwnd)
                if (
                        info[1] == os.getpid() and
                        IsWindowVisible(hwnd) and
                        IsWindowEnabled(hwnd)):
                    extra.append(hwnd)

            EnumWindows(callback, handles)
            active = GetActiveWindow()
            if active in handles:
                return active
            else:
                return None
        else:
            # XXX Todo: support for OS X and Gtk/Linux?
            return None

    def has_widget(self, text=None, type_=wx.Button):
        """ Return true if there is a widget of `type_` with `text`.

        """
        if text is None:
            test = None
        else:
            test = lambda widget: widget.GetLabelText() == text
        return self.find_widget(type_=type_, test=test) is not None

    def find_widget(self, type_=wx.Button, test=None):
        """ Return the widget of `type_` for which `test` returns true.

        """
        if test is None:
            test = lambda x: True
        window = self.get_dialog_widget()
        return find_widget(window, type_, test=test)
