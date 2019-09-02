# (C) Copyright 2014-2019 Enthought, Inc., Austin, TX
# All right reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import gc
import threading
from unittest import TestCase

import six

from traits.testing.unittest_tools import UnittestTools

from pyface.gui import GUI
from pyface.window import Window
from pyface.toolkit_utils import destroy_later, is_destroyed
from .event_loop_helper import ConditionTimeoutError, EventLoopHelper

if six.PY2:
    import mock
else:
    import unittest.mock as mock


class GuiTestCase(TestCase, UnittestTools):
    """ Base TestCase class for GUI test cases. """

    # ------------------------------------------------------------------------
    #  'GuiTestTools' protocol
    # ------------------------------------------------------------------------

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

    def assertToolkitControlDestroyedInGui(self, control, timeout=1.0):
        """
        Assert that the given toolkit control is destroyed if we run the GUI
        event loop for long enough.

        Parameters
        ----------
        controll : toolkit control
            The toolkit control being watched.
        timeout : float
            Maximum length of time to wait for the control to be destroyed,
            in seconds.

        Raises
        ------
        self.failureException
            If the control is not destroyed within the given timeout.
        """
        def condition():
            is_destroyed(control)

        try:
            self.event_loop_until_condition(condition, timeout)
        except ConditionTimeoutError:
            self.fail("Timed out waiting for control to be destroyed.")

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
        self.gui.call_later(callable)
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

    def event_loop_until_widget_destroyed(self, widget, timeout=10.0):
        """ Delete a widget and run the event loop.

        This doesn't actually delete the underlying control, just tests
        whether the widget still holds a reference to it.

        Parameters
        ----------
        widget : IWidget
            The widget to delete.
        timeout : float
            The number of seconds to run the event loop in the event that the
            widget is not deleted.

        Raises
        ------
        ConditionTimeoutError
            If the timeout occurs before the widget is deleted.
        """
        def condition():
            return widget.control is None

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
        def condition():
            is_destroyed(control)

        destroy_later(control)
        self.event_loop_until_condition(condition, timeout)

    # ------------------------------------------------------------------------
    #  'TestCase' protocol
    # ------------------------------------------------------------------------

    def setUp(self):
        """ Setup the test case for GUI interactions.
        """
        self.gui = GUI()
        self.app = self.gui.app
        self.event_loop_helper = EventLoopHelper(gui=self.gui)

        # Window.activate raises the window to the top by default.
        # On some OS this also activates the application, potentially
        # interrupting the user while the tests are running.
        # We patch the  Window.activate to never raise.
        wrapped_activate = Window.activate

        def new_activate(self, should_raise=True):
            wrapped_activate(self, False)

        self.pyface_raise_patch = mock.patch(
            Window.activate,
            new_callable=lambda: new_activate)
        self.pyface_raise_patch.start()

        super(GuiTestCase, self).setUp()

    def tearDown(self):
        """ Tear down the test case.

        This method attempts to ensure that there are no windows that
        remain open after the test case has run, and that there are no
        events in the event queue to minimize the likelihood of one test
        interfering with another.
        """
        # process events to clear out any remaining events left by
        # misbehaving tests
        self.event_loop_with_timeout(repeat=5)

        # Some top-level widgets may only be present due to cyclic garbage not
        # having been collected; force a garbage collection before we decide to
        # close windows. This may need several rounds.
        for _ in range(10):
            if not gc.collect():
                break

        # ensure any remaining top-level widgets get closed
        if self.gui.top_level_widgets():
            self.gui.invoke_later(self.gui.close_all, force=True)
            self.event_loop_helper.event_loop_with_timeout(repeat=5)

        # manually process events one last time
        self.gui.process_events()

        # uninstall the Pyface raise patch
        self.pyface_raise_patch.stop()

        # clean up objects to GC any remaining state
        del self.event_loop_helper
        del self.app
        del self.gui

        super(GuiTestCase, self).tearDown()