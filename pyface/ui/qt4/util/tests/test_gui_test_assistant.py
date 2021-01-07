# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import unittest

from pyface.timer.api import CallbackTimer
from pyface.ui.qt4.util.gui_test_assistant import GuiTestAssistant
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
