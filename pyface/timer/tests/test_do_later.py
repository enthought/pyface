from __future__ import print_function

import time
from unittest import TestCase, skipIf

from pyface.toolkit import toolkit_object
from ..i_timer import perf_counter
from ..do_later import DoLaterTimer, do_after, do_later

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


class ConditionHandler(object):
    def __init__(self):
        self.count = 0
        self.times = []

    def callback(self):
        self.times.append(perf_counter())
        self.count += 1


@skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestDoLaterTimer(TestCase, GuiTestAssistant):
    """ Test the DoLaterTimer. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
        start_time = perf_counter()
        timer = DoLaterTimer(100, handler.callback, (), {})

        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        self.assertEqual(handler.count, 1)

        expected_time = start_time + 0.1

        # give feedback in case of failure
        if expected_time > handler.times[0]:
            print(expected_time, handler.times)

        self.assertTrue(expected_time <= handler.times[0])


@skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
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


@skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestDoAfter(TestCase, GuiTestAssistant):
    """ Test do_after. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
        start_time = perf_counter()
        timer = do_after(100, handler.callback)

        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        self.assertEqual(handler.count, 1)

        expected_time = start_time + 0.1

        # give feedback in case of failure
        if expected_time > handler.times[0]:
            print(expected_time, handler.times)

        self.assertTrue(expected_time <= handler.times[0])
