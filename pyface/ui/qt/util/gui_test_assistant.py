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
import gc
import threading


import unittest.mock as mock

from pyface.qt.QtGui import QApplication
from pyface.ui.qt.gui import GUI
from traits.testing.api import UnittestTools
from traits.testing.unittest_tools import (
    _TraitsChangeCollector as TraitsChangeCollector,
)

from .testing import find_qt_widget
from .event_loop_helper import EventLoopHelper, ConditionTimeoutError


class GuiTestAssistant(UnittestTools):

    # 'TestCase' protocol -------------------------------------------------#

    def setUp(self):
        qt_app = QApplication.instance()
        if qt_app is None:
            qt_app = QApplication([])
        self.qt_app = qt_app
        self.gui = GUI()
        self.event_loop_helper = EventLoopHelper(
            qt_app=self.qt_app, gui=self.gui
        )
        try:
            import traitsui.api  # noqa: F401
        except ImportError:
            self.traitsui_raise_patch = None
        else:
            try:
                import traitsui.qt  # noqa: F401
                self.traitsui_raise_patch = mock.patch(
                    "traitsui.qt.ui_base._StickyDialog.raise_"
                )
            except ModuleNotFoundError:
                self.traitsui_raise_patch = mock.patch(
                    "traitsui.qt4.ui_base._StickyDialog.raise_"
                )
            self.traitsui_raise_patch.start()

        def new_activate(self):
            self.control.activateWindow()

        self.pyface_raise_patch = mock.patch(
            "pyface.ui.qt.window.Window.activate",
            new_callable=lambda: new_activate,
        )
        self.pyface_raise_patch.start()

    def tearDown(self):
        # Process any tasks that a misbehaving test might have left on the
        # queue.
        with self.event_loop_with_timeout(repeat=5):
            pass

        # Some top-level widgets may only be present due to cyclic garbage not
        # having been collected; force a garbage collection before we decide to
        # close windows. This may need several rounds.
        for _ in range(10):
            if not gc.collect():
                break

        if len(self.qt_app.topLevelWidgets()) > 0:
            with self.event_loop_with_timeout(repeat=5):
                self.gui.invoke_later(self.qt_app.closeAllWindows)

        self.pyface_raise_patch.stop()
        if self.traitsui_raise_patch is not None:
            self.traitsui_raise_patch.stop()

        del self.pyface_raise_patch
        del self.traitsui_raise_patch
        del self.event_loop_helper
        del self.gui
        del self.qt_app

    # 'GuiTestAssistant' protocol -----------------------------------------#

    @contextlib.contextmanager
    def event_loop(self, repeat=1):
        """Artificially replicate the event loop by Calling sendPostedEvents
        and processEvents ``repeat`` number of times. If the events to be
        processed place more events in the queue, begin increasing the value
        of ``repeat``, or consider using ``event_loop_until_condition``
        instead.

        Parameters
        ----------
        repeat : int
            Number of times to process events.
        """
        yield
        self.event_loop_helper.event_loop(repeat=repeat)

    @contextlib.contextmanager
    def delete_widget(self, widget, timeout=1.0):
        """Runs the real Qt event loop until the widget provided has been
        deleted.

        Parameters
        ----------
        widget : QObject
            The widget whose deletion will stop the event loop.
        timeout : float
            Number of seconds to run the event loop in the case that the
            widget is not deleted.
        """
        try:
            with self.event_loop_helper.delete_widget(widget, timeout=timeout):
                yield
        except ConditionTimeoutError:
            self.fail(
                "Could not destroy widget before timeout: {!r}".format(widget)
            )

    @contextlib.contextmanager
    def event_loop_until_condition(self, condition, timeout=10.0):
        """Runs the real Qt event loop until the provided condition evaluates
        to True.

        This should not be used to wait for widget deletion. Use
        delete_widget() instead.

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

        If the event loop exits before the condition evaluates to True or times
        out, a RuntimeWarning will be generated and the message will indicate
        whether the condition was ever successfully evaluated  or whether it
        always evalutated to False.

        Parameters
        ----------
        condition : Callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.
        timeout : float
            Number of seconds to run the event loop in the case that the
            condition is not satisfied.

            `timeout` is rounded to the nearest millisecond.
        """
        try:
            yield
            self.event_loop_helper.event_loop_until_condition(
                condition, timeout=timeout
            )
        except ConditionTimeoutError:
            self.fail("Timed out waiting for condition")

    def assertEventuallyTrueInGui(self, condition, timeout=10.0):
        """
        Assert that the given condition becomes true if we run the GUI
        event loop for long enough.

        Notes
        -----

        This assertion runs the real Qt event loop, polling the condition
        every 50 ms and returning as soon as the condition becomes true. If
        the condition does not become true within the given timeout, the
        assertion fails.

        Because the state of the condition is only polled every 50 ms, it
        may fail to detect transient states that appear and disappear within
        a 50 ms window.  Tests should ensure that any state that is being
        tested by the condition cannot revert to a False value once it becomes
        True.

        Parameters
        ----------
        condition : Callable() -> bool
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
            self.event_loop_helper.event_loop_until_condition(
                condition, timeout=timeout
            )
        except ConditionTimeoutError:
            self.fail("Timed out waiting for condition to become true.")

    @contextlib.contextmanager
    def assertTraitChangesInEventLoop(
        self, obj, trait, condition, count=1, timeout=10.0
    ):
        """Runs the real Qt event loop, collecting trait change events until
        the provided condition evaluates to True.

        Parameters
        ----------
        obj : traits.has_traits.HasTraits
            The HasTraits instance whose trait will change.
        trait : str
            The extended trait name of trait changes to listen to.
        condition : Callable
            A callable to determine if the stop criteria have been met. This
            takes obj as the only argument.
        count : int
            The expected number of times the event should be fired. The default
            is to expect one event.
        timeout : float
            Number of seconds to run the event loop in the case that the trait
            change does not occur.
        """
        condition_ = lambda: condition(obj)
        collector = TraitsChangeCollector(obj=obj, trait_name=trait)

        collector.start_collecting()
        try:
            try:
                yield collector
                self.event_loop_helper.event_loop_until_condition(
                    condition_, timeout=timeout
                )
            except ConditionTimeoutError:
                actual_event_count = collector.event_count
                msg = (
                    "Expected {} event on {} to be fired at least {} "
                    "times, but the event was only fired {} times "
                    "before timeout ({} seconds)."
                )
                msg = msg.format(
                    trait, obj, count, actual_event_count, timeout
                )
                self.fail(msg)
        finally:
            collector.stop_collecting()

    @contextlib.contextmanager
    def event_loop_until_traits_change(self, traits_object, *traits, **kw):
        """Run the real application event loop until a change notification for
        all of the specified traits is received.

        Paramaters
        ----------
        traits_object : traits.has_traits.HasTraits
            The object on which to listen for a trait events
        traits : one or more str
            The names of the traits to listen to for events
        timeout : float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.
        """
        timeout = kw.pop("timeout", 10.0)
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
            def handler(event):
                set_event(trait)

            return handler

        handlers = {trait: make_handler(trait) for trait in traits}

        for trait, handler in handlers.items():
            traits_object.observe(handler, trait)
        try:
            with self.event_loop_until_condition(
                condition=condition.is_set, timeout=timeout
            ):
                yield
        finally:
            for trait, handler in handlers.items():
                traits_object.observe(handler, trait, remove=True)

    @contextlib.contextmanager
    def event_loop_with_timeout(self, repeat=2, timeout=10.0):
        """Helper context manager to send all posted events to the event queue
        and wait for them to be processed.

        This differs from the `event_loop()` context manager in that it
        starts the real event loop rather than emulating it with
        `QApplication.processEvents()`

        Parameters
        ----------
        repeat : int
            Number of times to process events. Default is 2.
        timeout : float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.
        """
        yield
        self.event_loop_helper.event_loop_with_timeout(
            repeat=repeat, timeout=timeout
        )

    def find_qt_widget(self, start, type_, test=None):
        """Recursively walks the Qt widget tree from Qt widget `start` until it
        finds a widget of type `type_` (a QWidget subclass) that
        satisfies the provided `test` method.

        Parameters
        ----------
        start : QWidget
            The widget from which to start walking the tree
        type_ : type
            A subclass of QWidget to use for an initial type filter while
            walking the tree
        test : Callable
            A filter function that takes one argument (the current widget being
            evaluated) and returns either True or False to determine if the
            widget matches the required criteria.
        """
        return find_qt_widget(start, type_, test=test)
