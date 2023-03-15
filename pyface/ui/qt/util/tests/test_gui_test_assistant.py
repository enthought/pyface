# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import itertools
import unittest

from pyface.timer.api import CallbackTimer
from pyface.ui.qt.util.gui_test_assistant import GuiTestAssistant
from pyface.ui.qt.util.event_loop_helper import ConditionTimeoutError
from traits.api import Event, HasStrictTraits


class ExampleObject(HasStrictTraits):
    """ Test class; target for test_event_loop_until_traits_change. """

    spam = Event()
    eggs = Event()


class TestGuiTestAssistant(GuiTestAssistant, unittest.TestCase):
    def test_event_loop_until_traits_change_with_single_trait_success(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()

        # Successful case.
        with self.event_loop_until_traits_change(obj, "spam"):
            obj.spam = True

    def test_event_loop_until_traits_change_with_single_trait_failure(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()

        # Failing case.
        with self.assertRaises(AssertionError):
            with self.event_loop_until_traits_change(obj, "spam", timeout=0.1):
                obj.eggs = True

    def test_event_loop_until_traits_change_with_multiple_traits_success(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()
        with self.event_loop_until_traits_change(obj, "spam", "eggs"):
            obj.spam = True
            obj.eggs = True

    def test_event_loop_until_traits_change_with_multiple_traits_failure(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()
        with self.assertRaises(AssertionError):
            with self.event_loop_until_traits_change(
                obj, "spam", "eggs", timeout=0.1
            ):
                obj.eggs = True

        # event_loop_until_traits_change calls self.fail on timeout.
        with self.assertRaises(AssertionError):
            with self.event_loop_until_traits_change(
                obj, "spam", "eggs", timeout=0.1
            ):
                obj.spam = True

    def test_event_loop_until_traits_change_with_no_traits_success(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()

        # Successful case.
        with self.event_loop_until_traits_change(obj):
            pass

    def test_assert_eventually_true_in_gui_success(self):
        my_list = []

        timer = CallbackTimer(
            interval=0.05, callback=my_list.append, args=("bob",), repeat=1
        )

        timer.start()
        try:
            self.assertEventuallyTrueInGui(lambda: len(my_list) > 0)
            self.assertEqual(my_list, ["bob"])
        finally:
            timer.stop()

    def test_assert_eventually_true_in_gui_already_true(self):
        my_list = ["bob"]
        self.assertEventuallyTrueInGui(lambda: len(my_list) > 0)

    def test_assert_eventually_true_in_gui_failure(self):
        my_list = []
        with self.assertRaises(AssertionError):
            self.assertEventuallyTrueInGui(
                lambda: len(my_list) > 0, timeout=0.1
            )

    def test_assert_eventually_true_in_gui_dont_retest_immediately_true(self):
        # Given an always-True condition
        return_value_logs = []

        def logging_condition():
            return_value = True
            return_value_logs.append(return_value)
            return return_value

        # When we wait for the condition to become true
        self.assertEventuallyTrueInGui(logging_condition)

        # Then the condition should have been evaluated exactly once.
        self.assertEqual(return_value_logs, [True])

    def test_assert_eventually_true_in_gui_dont_retest_eventually_true(self):
        # Given a condition that returns two False values, followed by
        # infinitely many True values ...
        return_values = itertools.chain([False]*2, itertools.repeat(True))

        return_value_logs = []

        def logging_condition():
            return_value = next(return_values)
            return_value_logs.append(return_value)
            return return_value

        # When we wait for the condition to become true
        self.assertEventuallyTrueInGui(logging_condition)

        # Then the condition should not have been evaluated again after
        # becoming True.
        self.assertEqual(return_value_logs.count(True), 1)

    def test_event_loop_until_condition_early_exit(self):

        def condition():
            return False

        self.gui.invoke_after(1000, self.qt_app.exit)

        with self.assertWarns(RuntimeWarning) as cm:
            self.event_loop_helper.event_loop_until_condition(condition)

        self.assertIn("without condition evaluating to True", str(cm.warning))

    def test_event_loop_until_condition_timeout(self):

        def condition():
            return False

        with self.assertRaises(ConditionTimeoutError) as cm:
            self.event_loop_helper.event_loop_until_condition(condition, timeout=1.0)

        self.assertIn(
            "without condition evaluating to True",
            str(cm.exception),
        )
