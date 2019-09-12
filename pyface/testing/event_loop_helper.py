# (C) Copyright 2019 Enthought, Inc., Austin, TX
# All right reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!


import contextlib
import threading

from traits.api import HasStrictTraits, Instance

from pyface.gui import GUI
from pyface.i_gui import IGUI
from pyface.timer.api import CallbackTimer


class ConditionTimeoutError(RuntimeError):
    pass


class EventLoopHelper(HasStrictTraits):
    """ Toolkit-independent methods for running event loops in tests.
    """

    #: A reference to the GUI object
    gui = Instance(IGUI, factory=GUI)

    @contextlib.contextmanager
    def dont_quit_when_last_window_closed(self):
        """ Suppress exit of the application when the last window is closed.
        """
        flag = self.gui.quit_on_last_window_close
        self.gui.quit_on_last_window_close = False
        try:
            yield
        finally:
            self.gui.quit_on_last_window_close = flag

    def event_loop(self, repeat=1, allow_user_events=True):
        """ Emulate an event loop running ``repeat`` times.

        Parameters
        ----------
        repeat : positive int
            The number of times to call process events.  Default is 1.
        allow_user_events : bool
            Whether to process user-generated events.
        """
        for i in range(repeat):
            self.gui.process_events(allow_user_events)

    def event_loop_until_condition(self, condition, timeout=10.0):
        """ Run the event loop until condition returns true, or timeout.

        This runs the real event loop, rather than emulating it with
        :meth:`GUI.process_events`.  Conditions and timeouts are tracked
        using timers.

        Parameters
        ----------
        condition : callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.

        timeout : float
            Number of seconds to run the event loop in the case that the trait
            change does not occur.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the condition is True.
        """
        def callback():
            print('condition', condition, condition())
            if condition():
                self.gui.stop_event_loop()

        with self.dont_quit_when_last_window_closed():
            condition_timer = CallbackTimer.timer(
                callback=callback,
                interval=0.05,
            )
            timeout_timer = CallbackTimer.single_shot(
                callback=self.gui.stop_event_loop,
                interval=timeout,
            )

            try:
                self.gui.start_event_loop()
                if not condition():
                    raise ConditionTimeoutError(
                        'Timed out waiting for condition')
            finally:
                timeout_timer.stop()
                condition_timer.stop()

    def event_loop_with_timeout(self, repeat=2, timeout=10):
        """ Run the event loop at least repeat times in timeout seconds.

        This runs the real event loop but additionally ensures that all
        pending events get run at repeat times via gui.process_events.

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 2.
        timeout: float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the loop is repeated enough times.
        """
        condition = threading.Event()

        def repeat_loop(condition, repeat):
            """ Manually process events repeat times.
            """
            self.gui.process_events()
            print(repeat, condition.is_set())
            repeat = repeat - 1
            if repeat <= 0:
                self.gui.invoke_later(condition.set)
                print(repeat, condition.is_set())
            else:
                self.gui.invoke_later(
                    repeat_loop, condition=condition, repeat=repeat
                )

        self.gui.invoke_later(repeat_loop, repeat=repeat, condition=condition)

        self.event_loop_until_condition(
            condition=condition.is_set, timeout=timeout)
