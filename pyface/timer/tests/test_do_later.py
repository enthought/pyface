from __future__ import print_function

import time
from unittest import TestCase, skipIf

from pyface.toolkit import toolkit_object
from ..i_timer import perf_counter
from ..do_later import DoLaterTimer

GuiTestAssistant = toolkit_object('util.gui_test_assistant:GuiTestAssistant')
no_gui_test_assistant = (GuiTestAssistant.__name__ == 'Unimplemented')


class ConditionHandler(object):
    def __init__(self):
        self.count = 0
        self.times = []
        self.called = False

    def callback(self):
        self.times.append(perf_counter())
        self.count += 1
        self.called = True

    def is_called(self):
        return self.called

    def called_n(self, repeat):
        return lambda: self.count >= repeat


@skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestCallbackTimer(TestCase, GuiTestAssistant):
    """ Test the CallbackTimer. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
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

        expected_time = timer._start_time + 0.10

        # give feedback in case of failure
        if expected_time > handler.times[0]:
            print(handler.times)

        self.assertTrue(expected_time <= handler.times[0])
