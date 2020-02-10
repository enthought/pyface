
# (C) Copyright 2014-15 Enthought, Inc., Austin, TX
# All right reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Code modified from pyface.ui.qt4.util.event_loop_helper
import contextlib
import threading

import wx
from traits.api import HasStrictTraits, Instance
from pyface.api import GUI
from pyface.util.guisupport import start_event_loop_wx


class ConditionTimeoutError(RuntimeError):
    pass


@contextlib.contextmanager
def dont_quit_when_last_window_closed(wx_app):
    """
    Suppress exit of the application when the last window is closed.

    """
    flag = wx_app.GetExitOnFrameDelete()
    wx_app.SetExitOnFrameDelete(False)
    try:
        yield
    finally:
        wx_app.SetExitOnFrameDelete(flag)


class EventLoopHelper(HasStrictTraits):
    """ A helper class to provide basic event loop functionality. """

    #: The gui toolkit application.
    gui_app = Instance(wx.App)

    #: The pyface gui implementation
    gui = Instance(GUI, ())

    #: Reference to a dummy wx event handler that will help bind events for
    #: the timers.
    _handler = Instance(wx.EvtHandler, ())

    @contextlib.contextmanager
    def event_loop(self, repeat=1):
        """ Emulates an event loop `repeat` times.

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 1.

        """
        yield
        for i in range(repeat):
            self.gui_app.ProcessPendingEvents()

    def event_loop_until_condition(self, condition, start=None, timeout=10.0):
        """ Runs the real event loop until the provided condition evaluates
        to True.

        Raises ConditionTimeoutError if the timeout occurs before the condition
        is satisfied.

        Parameters
        ----------
        condition : callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.

        start : callable
            A callable to use in order to start the event loop. Default is
            to create a small frame or reuse the top level window if it is
            still available.

        timeout : float
            Number of seconds to run the event loop in the case that the trait
            change does not occur.

        """
        def handler(event):
            if condition():
                self.gui_app.Exit()

        # Make sure we don't get a premature exit from the event loop.
        with dont_quit_when_last_window_closed(self.gui_app):
            condition_timer = wx.Timer(self._handler)
            timeout_timer = wx.Timer(self._handler)
            self._handler.Bind(wx.EVT_TIMER, handler, condition_timer)
            self._handler.Bind(
                wx.EVT_TIMER,
                lambda event: self.gui_app.Exit(),
                timeout_timer
            )
            timeout_timer.Start(int(timeout * 1000), True)
            condition_timer.Start(50)
            try:
                if start is None:
                    self._start_event_loop()
                else:
                    start()
                if not condition():
                    raise ConditionTimeoutError(
                        'Timed out waiting for condition')
            finally:
                timeout_timer.Stop()
                condition_timer.Stop()

    @contextlib.contextmanager
    def delete_window(self, window, timeout=2.0):
        """ Runs the real event loop until the window provided has been deleted.

        Parameters
        ----------
        window :
            The toolkit window widget whose deletion will stop the event loop.

        timeout : float
            Number of seconds to run the event loop in the case that the
            widget is not deleted.

        Raises
        ------
        ConditionTimeoutError:
            Raised on timeout.

        """
        timer = wx.Timer(self._handler)
        self._handler.Bind(
            wx.EVT_TIMER,
            lambda event: self.gui_app.Exit(),
            timer
        )
        yield
        timer.Start(int(timeout * 1000), True)
        self._start_event_loop()
        if not timer.IsRunning():
            # We exited the event loop on timeout
            raise ConditionTimeoutError(
                'Could not destroy widget before timeout: {!r}'.format(window))

    def _start_event_loop(self):
        app = self.gui_app
        window = app.GetTopWindow()
        if window is None:
            # The wx EventLoop needs an active Window in order to work.
            window = wx.Frame(None, size=(1, 1))
            app.SetTopWindow(window)
        window.Show(True)
        start_event_loop_wx(app)
