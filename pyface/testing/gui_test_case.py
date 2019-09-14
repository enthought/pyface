# (C) Copyright 2014-2019 Enthought, Inc., Austin, TX
# All right reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from contextlib import contextmanager
import gc
import threading
from unittest import TestCase

import six

from traits.testing.unittest_tools import UnittestTools

from pyface.gui import GUI
from pyface.timer.timer import CallbackTimer
from pyface.window import Window
from pyface.toolkit_utils import destroy_later, is_destroyed
from .event_loop_helper import ConditionTimeoutError, EventLoopHelper

if six.PY2:
    import mock
else:
    import unittest.mock as mock


class GuiTestCase(UnittestTools, TestCase):
    """ Base TestCase class for GUI test cases. """

    # ------------------------------------------------------------------------
    #  'GuiTestTools' protocol
    # ------------------------------------------------------------------------

    # -- New Test "assert" methods ------------------------------------------

    def assertEventuallyTrueInGui(self, condition, timeout=10.0):
        """
        Assert that the given condition becomes true if we run the GUI
        event loop for long enough.

        This assertion runs the real GUI event loop, polling the condition
        and returning as soon as the condition becomes true. If the condition
        does not become true within the given timeout, the assertion fails.

        Parameters
        ----------
        condition : callable() -> bool
            Callable accepting no arguments and returning a bool.
        timeout : float
            Maximum length of time to wait for the condition to become
            true, in seconds.

        Raises
        ------
        self.failureException
            If the condition does not become true within the given timeout.
        """
        try:
            self.event_loop_until_condition(condition, timeout)
        except ConditionTimeoutError:
            self.fail("Timed out waiting for condition to become true.")

    def assertTraitsChangeInGui(self, object, *traits, **kw):
        """Run the real application event loop until a change notification for
        all of the specified traits is received.

        Paramaters
        ----------
        object : HasTraits instance
            The object on which to listen for a trait events
        traits : one or more str
            The names of the traits to listen to for events
        timeout : float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.
        """
        try:
            self.event_loop_until_traits_change(object, *traits, **kw)
        except ConditionTimeoutError:
            self.fail("Timed out waiting for traits to change.")

    def assertTraitValueInGui(self, object, trait, value, timeout=10.0):
        """
        Assert that the given trait assumes the specified value if we run the
        GUI event loop for long enough.

        Parameters
        ----------
        object : HasTraits instance
            The Traits object that holds the trait.
        trait : str
            The name of the trait being tested.
        value : any
            The value that the trait holds.
        timeout : float
            Maximum length of time to wait for the condition to become
            true, in seconds.

        Raises
        ------
        self.failureException
            If the condition does not become true within the given timeout.
        """
        def condition():
            return getattr(object, trait) == value

        try:
            self.event_loop_until_trait_value(object, trait, value, timeout)
        except ConditionTimeoutError:
            self.fail("Timed out waiting for trait to assume value.")

    def assertToolkitControlDestroyedInGui(self, control, timeout=1.0):
        """
        Assert that the given toolkit control is destroyed if we run the GUI
        event loop for long enough.

        Parameters
        ----------
        control : toolkit control
            The toolkit control being watched.
        timeout : float
            Maximum length of time to wait for the control to be destroyed,
            in seconds.

        Raises
        ------
        self.failureException
            If the control is not destroyed within the given timeout.
        """
        if control is None:
            return

        try:
            self.event_loop_until_control_destroyed(control, timeout)
        except ConditionTimeoutError:
            self.fail("Timed out waiting for control to be destroyed.")

    # -- Event loop methods -------------------------------------------------

    def set_trait_in_event_loop(self, object, trait, value, condition=None,
                                timeout=10):
        """ Start an event loop and set a trait to a value.

        By default this will stop the event loop when the trait is set to
        the value, but an optional condition can be used as a test
        instead. A timeout is also used if the condition does not become
        True.

        This is a blocking function.

        Parameters
        ----------
        object : HasTraits instance
            The object holding the trait value.
        trait : str
            The name of the trait.
        value : any
            The value being set on the trait.
        condition : callable or None
            A function that returns True when the event loop should stop.
            If None, then the event loop will stop when the value of the
            trait equals the supplied value.
        timeout : float
            The time in seconds before timing out.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the condition is True.
        """
        if condition is None:
            def condition():
                return getattr(object, trait) == value

        self.gui.set_trait_later(object, trait, value)
        self.event_loop_until_condition(condition, timeout)

    def invoke_in_event_loop(self, callable, condition, timeout=10):
        """ Start an event loop and call a function, stopping on condition.

        A timeout is used if the condition does not become True.

        Parameters
        ----------
        callable : callable
            The function to call.  It must expect no arguments, and any
            return value is ignored.
        condition : callable
            A function that returns True when the event loop should stop.
        timeout : float
            The time in seconds before timing out.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the condition is True.
        """
        self.gui.invoke_later(callable)
        self.event_loop_until_condition(condition, timeout)

    def event_loop_until_trait_value(self, object, trait, value, timeout=10.0):
        """Run the real application event loop until a change notification for
        all of the specified traits is received.

        Paramaters
        ----------
        traits_object : HasTraits instance
            The object on which to listen for a trait events
        traits : one or more str
            The names of the traits to listen to for events
        timeout : float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.
        """
        def condition():
            return getattr(object, trait) == value

        self.event_loop_until_condition(condition, timeout)

    def event_loop_until_traits_change(self, object, *traits, **kw):
        """Run the real application event loop until a change notification for
        all of the specified traits is received.

        Paramaters
        ----------
        traits_object : HasTraits instance
            The object on which to listen for a trait events
        traits : one or more str
            The names of the traits to listen to for events
        timeout : float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.
        """
        timeout = kw.pop('timeout', 10.0)
        condition = threading.Event()

        traits = set(traits)
        recorded_changes = set()

        # Correctly handle the corner case where there are no traits.
        if not traits:
            condition.set()

        def set_event(trait):
            recorded_changes.add(trait)
            if recorded_changes == traits:
                condition.set()

        def make_handler(trait):
            def handler():
                set_event(trait)
            return handler

        handlers = {trait: make_handler(trait) for trait in traits}

        for trait, handler in handlers.items():
            object.on_trait_change(handler, trait)
        try:
            self.event_loop_until_condition(condition.is_set, timeout)
        finally:
            for trait, handler in handlers.items():
                object.on_trait_change(handler, trait, remove=True)

    def event_loop_until_control_destroyed(self, control, timeout=10.0):
        """ Run the event loop until a control is destroyed.

        This doesn't actually delete the underlying control, just tests
        whether the widget still holds a reference to it.

        Parameters
        ----------
        control : toolkit control
            The widget to ensure is destroyed.
        timeout : float
            The number of seconds to run the event loop in the event that the
            toolkit control is not deleted.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the control is deleted.
        """
        def condition():
            return is_destroyed(control)

        self.event_loop_until_condition(condition, timeout)

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
            Number of seconds to run the event loop in the case that the
            condition does not occur.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the condition is True.
        """
        self.event_loop_helper.event_loop_until_condition(condition, timeout)

    def event_loop_with_timeout(self, repeat=1, timeout=10):
        """ Run the event loop for timeout seconds.
        """
        self.event_loop_helper.event_loop_with_timeout(repeat, timeout)

    def destroy_control(self, control, timeout=1.0):
        """ Schedule a toolkit control for destruction and run the event loop.

        Parameters
        ----------
        control : toolkit control
            The control to destroy.
        timeout : float
            The number of seconds to run the event loop in the event that the
            control is not destroyed.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the widget is destroyed.
        """
        destroy_later(control)
        self.event_loop_until_control_destroyed(control, timeout)

    def destroy_widget(self, widget, timeout=1.0):
        """ Schedule a Widget for destruction and run the event loop.

        Parameters
        ----------
        control : IWidget
            The widget to destroy.
        timeout : float
            The number of seconds to run the event loop in the event that the
            widget is not destroyed.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the widget is destroyed.
        """
        if widget.control is not None:
            control = widget.control
            widget.destroy()
            self.event_loop_until_control_destroyed(control, timeout)

    # ------------------------------------------------------------------------
    #  'TestCase' protocol
    # ------------------------------------------------------------------------

    def setUp(self):
        """ Setup the test case for GUI interactions.
        """
        self.gui = GUI()
        self.app = self.gui.app
        self.event_loop_helper = EventLoopHelper(gui=self.gui)

        self.gui.quit_on_last_window_close = False

        # clean-up actions (LIFO)
        self.addCleanup(self._delete_attrs, "gui", "app", "event_loop_helper")
        self.addCleanup(self._restore_quit_on_last_window_close)
        self.addCleanup(self.gui.clear_event_queue)
        self.addCleanup(self.gui.process_events)
        self.addCleanup(self._close_top_level_windows)
        self.addCleanup(self._gc_collect)
        self.addCleanup(self.event_loop_helper.event_loop, 5, False)

        super(GuiTestCase, self).setUp()

    def tearDown(self):
        """ Tear down the test case.

        This method attempts to ensure that there are no windows that
        remain open after the test case has run, and that there are no
        events in the event queue to minimize the likelihood of one test
        interfering with another.
        """

        super(GuiTestCase, self).tearDown()

    def _gc_collect(self):
        # Some top-level widgets may only be present due to cyclic garbage not
        # having been collected; force a garbage collection before we decide to
        # close windows. This may need several rounds.
        for _ in range(10):
            if not gc.collect():
                break

    def _close_top_level_windows(self):
        # clean
        if self.gui.top_level_windows():
            def on_stop(active):
                if not active:
                    self.gui.stop_event_loop()

            repeat_timer = CallbackTimer(
                repeat=5,
                callback=self.gui.close_all,
                kwargs={'force': True}
            )
            repeat_timer.start()
            self.event_loop_helper.event_loop_with_timeout(timeout=1)
            del repeat_timer

    def _restore_quit_on_last_window_close(self):
        self.gui.quit_on_last_window_close = True

    def _delete_attrs(self, *attrs):
        # clean up objects to GC any remaining state
        for attr in attrs:
            delattr(self, attr)
