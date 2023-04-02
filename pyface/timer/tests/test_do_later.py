# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from unittest import TestCase, skipIf

from pyface.toolkit import toolkit_object
from ..i_timer import perf_counter
from ..do_later import DoLaterTimer, do_after, do_later

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"


class ConditionHandler(object):
    def __init__(self):
        self.count = 0
        self.times = []

    def callback(self):
        self.times.append(perf_counter())
        self.count += 1


@skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestDoLaterTimer(TestCase, GuiTestAssistant):
    """ Test the DoLaterTimer. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
        start_time = perf_counter()
        length = 500
        timer = DoLaterTimer(length, handler.callback, (), {})

        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        self.assertEqual(handler.count, 1)

        # should take no less than 85% of time requested
        expected_length = (length / 1000.0) * 0.85
        expected_time = start_time + expected_length

        self.assertLessEqual(
            expected_time,
            handler.times[0],
            "Expected call after {} seconds, took {} seconds)".format(
                expected_length, handler.times[0] - start_time
            ),
        )


@skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestDoLater(TestCase, GuiTestAssistant):
    """ Test do_later. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
        timer = do_later(handler.callback)

        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        self.assertEqual(handler.count, 1)


@skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestDoAfter(TestCase, GuiTestAssistant):
    """ Test do_after. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
        start_time = perf_counter()
        length = 500
        timer = do_after(length, handler.callback)

        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        self.assertEqual(handler.count, 1)

        # should take no less than 85% of time requested
        expected_length = (length / 1000.0) * 0.85
        expected_time = start_time + expected_length

        self.assertLessEqual(
            expected_time,
            handler.times[0],
            "Expected call after {} seconds, took {} seconds)".format(
                expected_length, handler.times[0] - start_time
            ),
        )
