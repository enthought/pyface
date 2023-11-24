# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import contextlib
import threading
import warnings

from pyface.i_gui import IGUI
from pyface.qt import QtCore, QtGui
from traits.api import HasStrictTraits, Instance


class ConditionTimeoutError(RuntimeError):
    pass


@contextlib.contextmanager
def dont_quit_when_last_window_closed(qt_app):
    """
    Suppress exit of the application when the last window is closed.

    """
    flag = qt_app.quitOnLastWindowClosed()
    qt_app.setQuitOnLastWindowClosed(False)
    try:
        yield
    finally:
        qt_app.setQuitOnLastWindowClosed(flag)


class EventLoopHelper(HasStrictTraits):

    qt_app = Instance(QtGui.QApplication)

    gui = Instance(IGUI)

    def event_loop_with_timeout(self, repeat=2, timeout=10.0):
        """Helper function to send all posted events to the event queue and
        wait for them to be processed.  This runs the real event loop and
        does not emulate it with QApplication.processEvents.

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 2.
        timeout: float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.

        Notes
        -----
            `timeout` is rounded to the nearest millisecond.
        """

        def repeat_loop(condition, repeat):
            # We sendPostedEvents to ensure that enaml events are processed
            self.qt_app.sendPostedEvents()
            repeat = repeat - 1
            if repeat <= 0:
                self.gui.invoke_later(condition.set)
            else:
                self.gui.invoke_later(
                    repeat_loop, condition=condition, repeat=repeat
                )

        condition = threading.Event()
        self.gui.invoke_later(repeat_loop, repeat=repeat, condition=condition)
        self.event_loop_until_condition(
            condition=condition.is_set, timeout=timeout
        )

    def event_loop(self, repeat=1):
        """Emulates an event loop `repeat` times with
        QApplication.processEvents.

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 1.
        """
        for i in range(repeat):
            self.qt_app.sendPostedEvents()
            self.qt_app.processEvents()

    def event_loop_until_condition(self, condition, timeout=10.0):
        """Runs the real Qt event loop until the provided condition evaluates
        to True.

        Notes
        -----

        This runs the real Qt event loop, polling the condition every 50 ms and
        returning as soon as the condition becomes true. If the condition does
        not become true within the given timeout, a ConditionTimeoutError is
        raised.

        Because the state of the condition is only polled every 50 ms, it
        may fail to detect transient states that appear and disappear within
        a 50 ms window.  Code should ensure that any state that is being
        tested by the condition cannot revert to a False value once it becomes
        True.

        Parameters
        ----------
        condition : Callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.

        timeout : float
            Number of seconds to run the event loop in the case that the trait
            change does not occur.

            `timeout` is rounded to the nearest millisecond.

        Raises
        ------

        Raises ConditionTimeoutError if the timeout occurs before the condition
        is satisfied.  If the event loop exits before the condition evaluates
        to True or times out, a RuntimeWarning will be generated.

        In either of these cases, the message will indicate whether the
        condition was ever successfully evaluated (which may indicate an error
        in the condition's code) or whether it always evalutated to False.
        """

        condition_result = None
        timed_out = False

        def handler():
            nonlocal condition_result

            condition_result = bool(condition_result or condition())
            if condition_result:
                self.qt_app.exit()

        def do_timeout():
            nonlocal timed_out

            timed_out = True
            self.qt_app.exit()

        # Make sure we don't get a premature exit from the event loop.
        with dont_quit_when_last_window_closed(self.qt_app):
            condition_timer = QtCore.QTimer()
            condition_timer.setInterval(50)
            condition_timer.timeout.connect(handler)
            timeout_timer = QtCore.QTimer()
            timeout_timer.setSingleShot(True)
            timeout_timer.setInterval(round(timeout * 1000))
            timeout_timer.timeout.connect(do_timeout)
            timeout_timer.start()
            condition_timer.start()
            try:
                if hasattr(self.qt_app, 'exec'):
                    self.qt_app.exec()
                else:
                    self.qt_app.exec_()
                if not condition_result:
                    if condition_result is None:
                        status = "without evaluating condition"
                    else:
                        status = "without condition evaluating to True"
                    if timed_out:
                        raise ConditionTimeoutError(f"Timed out {status}.")
                    else:
                        warnings.warn(
                            RuntimeWarning(
                                f"Event loop exited early {status}."
                            )
                        )
            finally:
                timeout_timer.stop()
                condition_timer.stop()

    @contextlib.contextmanager
    def delete_widget(self, widget, timeout=1.0):
        """Runs the real Qt event loop until the widget provided has been
        deleted.  Raises ConditionTimeoutError on timeout.

        Parameters
        ----------
        widget : QObject
            The widget whose deletion will stop the event loop.

        timeout : float
            Number of seconds to run the event loop in the case that the
            widget is not deleted.

        Notes
        -----
            `timeout` is rounded to the nearest millisecond.
        """
        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.setInterval(round(timeout * 1000))
        timer.timeout.connect(self.qt_app.quit)
        widget.destroyed.connect(self.qt_app.quit)
        yield
        timer.start()
        if hasattr(self.qt_app, 'exec'):
            self.qt_app.exec()
        else:
            self.qt_app.exec_()
        if not timer.isActive():
            # We exited the event loop on timeout
            raise ConditionTimeoutError(
                "Could not destroy widget before timeout: {!r}".format(widget)
            )
