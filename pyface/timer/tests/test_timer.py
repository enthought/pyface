from __future__ import print_function
import time
from unittest import TestCase, skipIf

from pyface.toolkit import toolkit_object
from ..i_timer import perf_counter
from ..timer import CallbackTimer, EventTimer, Timer

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
class TestEventTimer(TestCase, GuiTestAssistant):
    """ Test the EventTimer. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        timer = EventTimer()

        self.assertIsNone(timer.repeat)
        self.assertFalse(timer.active)
        timer.start()
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.active)
        finally:
            timer.stop()
        self.assertFalse(timer.active)

    def test_timer_method(self):
        timer = EventTimer.timer()
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.active)
        finally:
            timer.stop()
        self.assertFalse(timer.active)

    def test_single_shot_method(self):
        timer = EventTimer.single_shot()
        handler = ConditionHandler()
        timer.on_trait_change(handler.callback, 'timeout')
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()
        self.assertFalse(timer.active)
        self.assertEqual(handler.count, 1)

    def test_set_active(self):
        timer = EventTimer()

        self.assertIsNone(timer.repeat)
        self.assertFalse(timer.active)
        timer.active = True
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.active)
        finally:
            timer.active = False
        self.assertFalse(timer.active)

    def test_timeout_event(self):
        timer = EventTimer()
        handler = ConditionHandler()
        timer.on_trait_change(handler.callback, 'timeout')

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                handler.is_called
            )
        finally:
            timer.stop()

    def test_repeat(self):
        timer = EventTimer(repeat=4)
        handler = ConditionHandler()
        timer.on_trait_change(handler.callback, 'timeout')

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()
        self.assertEqual(handler.count, 4)

    def test_interval(self):
        timer = EventTimer(repeat=4, interval=0.1)
        handler = ConditionHandler()
        timer.on_trait_change(handler.callback, 'timeout')

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()
        self.assertEqual(handler.count, 4)

        expected_times = [timer._start_time + 0.1 * i + 0.1 for i in range(4)]

        # give feedback in case of failure
        if not all(
            expected <= actual
            for expected, actual in zip(expected_times, handler.times)
        ):
            print(handler.times)

        self.assertTrue(
            all(
                expected <= actual
                for expected, actual in zip(expected_times, handler.times)
            )
        )

    def test_expire(self):
        timer = EventTimer(expire=1.0, interval=0.1)
        handler = ConditionHandler()
        timer.on_trait_change(handler.callback, 'timeout')

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        # give feedback in case of failure
        if not all(
            t < timer._start_time + timer.expire + 0.01 for t in handler.times
        ):
            print(handler.times[-1], timer._start_time + timer.expire)

        self.assertTrue(
            all(
                t < timer._start_time + timer.expire + 0.01
                for t in handler.times
            )
        )


@skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestCallbackTimer(TestCase, GuiTestAssistant):
    """ Test the CallbackTimer. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()
        timer = CallbackTimer(callback=handler.callback)

        self.assertIsNone(timer.repeat)
        self.assertFalse(timer.active)
        timer.start()
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.active)
        finally:
            timer.stop()
        self.assertFalse(timer.active)

    def test_timer_method(self):
        handler = ConditionHandler()

        timer = CallbackTimer.timer(callback=handler.callback)
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.active)
        finally:
            timer.stop()
        self.assertFalse(timer.active)

    def test_single_shot_method(self):
        handler = ConditionHandler()

        timer = CallbackTimer.single_shot(callback=handler.callback)
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()
        self.assertFalse(timer.active)
        self.assertEqual(handler.count, 1)

    def test_set_active(self):
        handler = ConditionHandler()
        timer = CallbackTimer(callback=handler.callback)

        self.assertIsNone(timer.repeat)
        self.assertFalse(timer.active)
        timer.active = True
        try:
            self.assertTrue(timer.active)
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.active)
        finally:
            timer.active = False
        self.assertFalse(timer.active)

    def test_timeout_event(self):
        handler = ConditionHandler()
        timer = CallbackTimer(callback=handler.callback)

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                handler.is_called
            )
        finally:
            timer.stop()

    def test_repeat(self):
        handler = ConditionHandler()
        timer = CallbackTimer(callback=handler.callback, repeat=4)

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()
        self.assertEqual(handler.count, 4)

    def test_interval(self):
        handler = ConditionHandler()
        timer = CallbackTimer(
            callback=handler.callback, repeat=4, interval=0.1
        )

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()
        self.assertEqual(handler.count, 4)

        expected_times = [timer._start_time + 0.1 * i + 0.1 for i in range(4)]

        # give feedback in case of failure
        if not all(
            expected <= actual
            for expected, actual in zip(expected_times, handler.times)
        ):
            print(handler.times)

        self.assertTrue(
            all(
                expected <= actual
                for expected, actual in zip(expected_times, handler.times)
            )
        )

    def test_expire(self):
        handler = ConditionHandler()
        timer = CallbackTimer(
            callback=handler.callback, interval=0.1, expire=1.0
        )

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()

        # give feedback in case of failure
        if not all(
            t < timer._start_time + timer.expire + 0.01 for t in handler.times
        ):
            print(handler.times[-1], timer._start_time + timer.expire)

        self.assertTrue(
            all(
                t < timer._start_time + timer.expire + 0.01
                for t in handler.times
            )
        )

    def test_stop_iteration(self):
        def do_stop_iteration():
            raise StopIteration()

        timer = CallbackTimer(callback=do_stop_iteration)

        timer.start()
        try:
            self.event_loop_helper.event_loop_until_condition(
                lambda: not timer.active
            )
            self.assertFalse(timer.active)
        finally:
            timer.stop()


@skipIf(no_gui_test_assistant, 'No GuiTestAssistant')
class TestTimer(TestCase, GuiTestAssistant):
    """ Test the CallbackTimer. """

    def setUp(self):
        GuiTestAssistant.setUp(self)

    def tearDown(self):
        GuiTestAssistant.tearDown(self)

    def test_basic(self):
        handler = ConditionHandler()

        timer = Timer(250, handler.callback)
        try:
            self.assertTrue(timer.IsRunning())
            self.event_loop_helper.event_loop()
            self.assertTrue(timer.IsRunning())
        finally:
            timer.Stop()

        self.assertFalse(timer.IsRunning())

    def test_restart(self):
        handler = ConditionHandler()

        timer = Timer(20, handler.callback)
        timer.Stop()

        # Ensure that it is indeed stopped.
        self.assertFalse(timer.IsRunning())
        count = handler.count

        # Wait to see if the timer has indeed stopped.
        self.event_loop_helper.event_loop()
        time.sleep(0.1)
        self.assertEqual(handler.count, count)

        timer.Start()
        try:
            self.assertTrue(timer.IsRunning())
            self.event_loop_helper.event_loop_until_condition(
                lambda: handler.count > count
            )
            self.assertTrue(timer.IsRunning())
        finally:
            timer.Stop()

        self.assertFalse(timer.IsRunning())

    def test_repeat(self):
        handler = ConditionHandler()

        start_time = perf_counter()
        timer = Timer(250, handler.callback)
        try:
            self.assertTrue(timer.IsRunning())
            self.event_loop_helper.event_loop_until_condition(
                handler.called_n(4)
            )
            self.assertTrue(timer.IsRunning())
        finally:
            timer.Stop()

        self.assertFalse(timer.IsRunning())

        self.assertEqual(handler.count, 4)

        expected_times = [start_time + 0.2 * i + 0.2 for i in range(4)]

        self.assertTrue(
            all(
                actual >= expected
                for actual, expected in zip(handler.times, expected_times)
            ),
            "Expected calls after {} times, got {})".format(
                expected_times,
                handler.times
            )
        )
