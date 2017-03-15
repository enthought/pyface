# --------------------------------------------------------------------------
#
#  Copyright (c) 2012-14, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in /LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  code based on the traits-enaml.testing.gui_test_assistant
#
# ---------------------------------------------------------------------------
import contextlib
import threading

import wx

from traits.testing.unittest_tools import UnittestTools
from traits.testing.unittest_tools import _TraitsChangeCollector as \
    TraitsChangeCollector
from pyface.util.guisupport import get_app_wx

from .event_loop_helper import EventLoopHelper, ConditionTimeoutError


def find_widget(start, type_, test=None):
    """Recursively walks the widget tree from widget `start` until it
       finds a widget of type `type_` (a toolkit widget subclass) that
        satisfies the provided `test` method.

       Parameters
       ----------
       start :
          The toolkit widget from which to start walking the tree
       type_ : type
           A subclass of toolkit widget to use for an initial type filter
           while walking the tree
       test : callable
           A filter function that takes one argument (the current widget being
           evaluated) and returns either True or False to determine if the
           widget matches the required criteria.

    """
    if test is None:
        test = lambda widget: True
    if isinstance(start, type_):
        if test(start):
            return start
    for child in start.GetChildren():
        widget = find_widget(child, type_, test=test)
        if widget:
            return widget
    return None


def print_widget_tree(widget, level=0):
    """ Debugging helper to print out the widget tree starting at a
    particular `widget`.

    Parameters
    ----------
    widget :
        The root widget in the tree to print.
    level : int
        The current level in the tree. Used internally for displaying the
        tree level.
    """
    level = level + 4
    if level == 0:
        print
    print ' '*level, widget
    for child in widget.GetChildren():
        print_widget_tree(child, level=level)
    if level == 0:
        print


class GuiTestAssistant(UnittestTools):

    def setUp(self):
        # Make sure that we have a running application.
        self.gui_app = get_app_wx()
        wx.Log.SetActiveTarget(wx.LogStderr())
        self.event_loop_helper = EventLoopHelper(gui_app=self.gui_app)

    def tearDown(self):
        windows = wx.GetTopLevelWindows()
        titles = []
        if len(windows) > 0:
            for window in windows:
                titles.append(window.GetTitle())

        def _cleanup():
            for window in wx.GetTopLevelWindows():
                window.Destroy()
                wx.WakeUpIdle()

        wx.CallLater(50, _cleanup)
        self.gui_app.MainLoop()
        if len(titles) > 0:
            raise RuntimeError(
                'Not all windows closed after test method, {}'.format(titles))
        del self.event_loop_helper
        del self.gui_app

    @contextlib.contextmanager
    def event_loop(self, repeat=1):
        """ Artificially replicate the event loop by processing events.

        If the events to be processed place more events in the queue,
        begin increasing the value of ``repeat``, or consider using
        ``event_loop_until_condition`` instead.

        Parameters
        ----------
        repeat : int
            Number of times to process events.

        """
        yield
        self.event_loop_helper.event_loop(repeat=repeat)

    @contextlib.contextmanager
    def delete_window(self, window, timeout=1.0):
        """Runs the real event loop until the widget provided has been deleted.

        Parameters
        ----------
        widget :
            The widget whose deletion will stop the event loop.

        timeout : float
            Number of seconds to run the event loop in the case that the
            widget is not deleted.

        """
        try:
            with self.event_loop_helper.delete_window(window, timeout=timeout):
                yield
        except ConditionTimeoutError:
            self.fail('Could not destroy window before timeout: {!r}'.format(
                window))

    @contextlib.contextmanager
    def event_loop_until_condition(self, condition, timeout=10.0):
        """Runs the real event loop until the provided condition evaluates
        to True.

        This should not be used to wait for widget deletion. Use
        delete_widget() instead.

        Parameters
        ----------
        condition : callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.

        timeout : float
            Number of seconds to run the event loop in the case that the
            condition is not satisfied.

        """
        try:
            yield
            self.event_loop_helper.event_loop_until_condition(
                condition, timeout=timeout)
        except ConditionTimeoutError:
            self.fail('Timed out waiting for condition')

    @contextlib.contextmanager
    def assertTraitChangesInEventLoop(
            self, obj, trait, condition, count=1, timeout=10.0):
        """Runs the real event loop, collecting trait change events until
        the provided condition evaluates to True.

        Parameters
        ----------
        obj : HasTraits
            The HasTraits instance whose trait will change.

        trait : str
            The extended trait name of trait changes to listen too.

        condition : callable
            A callable to determine if the stop criteria have been met. This
            should accept no arguments.

        count : int
            The expected number of times the event should be fired. The default
            is to expect one event.

        timeout : float
            Number of seconds to run the event loop in the case that the trait
            change does not occur.

        """
        condition_ = lambda: condition(obj)
        collector = TraitsChangeCollector(obj=obj, trait=trait)

        collector.start_collecting()
        try:
            try:
                yield collector
                self.event_loop_helper.event_loop_until_condition(
                    condition_, timeout=timeout)
            except ConditionTimeoutError:
                actual_event_count = collector.event_count
                msg = ("Expected {} event on {} to be fired at least {} "
                       "times, but the event was only fired {} times "
                       "before timeout ({} seconds).")
                msg = msg.format(
                    trait, obj, count, actual_event_count, timeout)
                self.fail(msg)
        finally:
            collector.stop_collecting()

    @contextlib.contextmanager
    def event_loop_until_traits_change(self, traits_object, *traits, **kw):
        """Run the real application event loop until a change notification for
        all of the specified traits is received.

        Parameters
        ----------
        traits_object: HasTraits instance
            The object on which to listen for a trait events
        traits: one or more str
            The names of the traits to listen to for events
        timeout: float, optional, keyword only
            Number of seconds to run the event loop in the case that the trait
            change does not occur. Default value is 10.0.

        """
        timeout = kw.pop('timeout', 10.0)
        condition = threading.Event()

        traits = set(traits)
        recorded_changes = set()

        def set_event(trait):
            recorded_changes.add(trait)
            if recorded_changes == traits:
                condition.set()

        handlers = {}
        for trait in traits:
            handlers[trait] = lambda: set_event(trait)

        for trait, handler in handlers.iteritems():
            traits_object.on_trait_change(handler, trait)
        try:
            with self.event_loop_until_condition(
                    condition=condition.is_set, timeout=timeout):
                yield
        finally:
            for trait, handler in handlers.iteritems():
                traits_object.on_trait_change(handler, trait, remove=True)

    @contextlib.contextmanager
    def wait_until_window_is_closed(self, timeout=10.0):
        """ Wait until the top window has closed and the application exits.

        """
        def condition(self):
            return self.gui_app.GetTopWindow() is None

        try:
            with self.event_loop_helper.event_loop_until_condition(
                    condition, timeout=timeout):
                yield
        except ConditionTimeoutError:
            self.fail('Timed out waiting for the application to exit')
