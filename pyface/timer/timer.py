# Author: Prabhu Ramachandran
# Copyright (c) 2006-2018,  Enthought, Inc.
# License: BSD Style.
"""
Event-loop based timers that perform actions periodically.

Note that if a timer goes out of scope without a reference to being saved,
there is nothing keeping the underlying toolkit timer alive and it will be
garbage collected, meaning that the timer will stop firing (or indeed, may
never fire).
"""

from pyface.toolkit import toolkit_object
from pyface.timer.i_timer import MCallbackTimer, MEventTimer

PyfaceTimer = toolkit_object('timer.timer:PyfaceTimer')


class EventTimer(MEventTimer, PyfaceTimer):
    pass


class CallbackTimer(MCallbackTimer, PyfaceTimer):
    pass


class Timer(CallbackTimer):
    """ Subclass of CallbackTimer that matches the old API """

    def __init__(self, millisecs, callable, *args, **kwargs):
        """ Initialize and start the timer.

        Initialize instance to invoke the given `callable` with given
        arguments and keyword args after every `millisecs` (milliseconds).
        """
        interval = millisecs / 1000.0
        super(Timer, self).__init__(
            interval=interval,
            callback=callable,
            args=args,
            kwargs=kwargs,
        )
        self.start()

    def Notify(self):
        """ Alias for `perform` to match old API.
        """
        self.perform()

    def Start(self, millisecs=None):
        """ Alias for `start` to match old API.
        """
        if millisecs is not None:
            self.interval = millisecs / 1000.0

        self.start()

    def Stop(self):
        """ Alias for `stop` to match old API.
        """
        self.stop()

    def IsRunning(self):
        """ Alias for is_running property to match old API.
        """
        return self._active
