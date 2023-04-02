# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Interfaces and base classes for cross-toolkit timers

This module defines interfaces for toolkit event-loop based timers.  It also
provides a base implementation that can be easily specialized for a particular
back-end, and mixins that provide additional capabilities.
"""
from abc import abstractmethod
import time

from traits.api import (
    ABCHasTraits,
    Bool,
    Callable,
    Dict,
    Event,
    Float,
    HasTraits,
    Int,
    Interface,
    Property,
    Range,
    Tuple,
    provides,
    Union,
)

perf_counter = time.perf_counter


class ITimer(Interface):
    """ Interface for timer classes.

    This is a base interface which doesn't specify any particular notification
    mechanism.
    """

    # ITimer interface -------------------------------------------------------

    #: The interval at which to call the callback in seconds.
    interval = Range(low=0.0)

    #: The number of times to repeat the callback, or None if no limit.
    repeat = Union(None, Int)

    #: The maximum length of time to run in seconds, or None if no limit.
    expire = Union(None, Float)

    #: Whether or not the timer is currently running.
    active = Bool()

    # -------------------------------------------------------------------------
    # ITimer interface
    # -------------------------------------------------------------------------

    @classmethod
    def timer(cls, **traits):
        """ Convenience method that creates and starts a timer.
        """
        pass

    @classmethod
    def single_shot(cls, **traits):
        """ Convenience method that creates and starts a single-shot timer.
        """
        pass

    def start(self):
        """ Start the timer. """
        pass

    def stop(self):
        """ Stop the timer. """
        pass

    def perform(self):
        """ The method that will be called by the timer. """
        pass


class IEventTimer(ITimer):
    """ Interface for timers which fire a trait event periodically. """

    # IEventTimer interface --------------------------------------------------

    #: A traits Event to fire when the callback happens.
    timeout = Event()


class ICallbackTimer(ITimer):
    """ Interface for timers which call a callback periodically. """

    # ICallbackTimer interface -----------------------------------------------

    #: The callback to make, or None if no callback.
    callback = Callable

    #: Positional arguments to give the callback.
    args = Tuple()

    #: Keyword arguments to give the callback.
    kwargs = Dict()


@provides(ITimer)
class BaseTimer(ABCHasTraits):
    """ Base class for timer classes.

    This class has a class variable which tracks active timers to prevent
    failures caused by garbage collection.  A timer is added to this tracker
    when it is started if the repeat value is not None.
    """

    # BaseTimer interface ----------------------------------------------------

    #: Class variable tracking all active timers.
    _active_timers = set()

    # ITimer interface -------------------------------------------------------

    #: The interval at which to call the callback in seconds.
    interval = Range(low=0.0, value=0.05)

    #: The number of times to repeat the callback, or None if no limit.
    repeat = Union(None, Int)

    #: The maximum length of time to run in seconds, or None if no limit.
    expire = Union(None, Float)

    #: Property that controls the state of the timer.
    active = Property(Bool, observe="_active")

    # Private interface ------------------------------------------------------

    #: Whether or not the timer is currently running.
    _active = Bool()

    #: The most recent start time.
    _start_time = Float()

    # -------------------------------------------------------------------------
    # ITimer interface
    # -------------------------------------------------------------------------

    @classmethod
    def timer(cls, **traits):
        """ Convenience method that creates and starts a timer.
        """
        timer = cls(**traits)
        timer.start()
        return timer

    @classmethod
    def single_shot(cls, **traits):
        timer = cls(repeat=1, **traits)
        timer.start()
        return timer

    def start(self):
        """ Start the timer. """
        if not self._active:
            if self.repeat is not None:
                self._active_timers.add(self)
            if self.expire is not None:
                self._start_time = perf_counter()
            self._active = True
            self._start()

    def stop(self):
        """ Stop the timer. """
        if self._active:
            self._active_timers.discard(self)
            self._stop()
            self._active = False

    def perform(self):
        """ Perform the callback.

        The timer will stop if repeats is not None and less than 1, or if
        the `_perform` method raises StopIteration.
        """
        if self.expire is not None:
            if perf_counter() - self._start_time > self.expire:
                self.stop()
                return

        if self.repeat is not None:
            self.repeat -= 1

        try:
            self._perform()
        except StopIteration:
            self.stop()
        except:
            self.stop()
            raise
        else:
            if self.repeat is not None and self.repeat <= 0:
                self.stop()
                self.repeat = 0

    # BaseTimer Protected methods

    def _start(self):
        """ Start the toolkit timer.

        Subclasses should overrided this method.
        """
        raise NotImplementedError()

    def _stop(self):
        """ Stop the toolkit timer.

        Subclasses should overrided this method.
        """
        raise NotImplementedError()

    @abstractmethod
    def _perform(self):
        """ perform the appropriate action.

        Subclasses should overrided this method.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Private interface
    # -------------------------------------------------------------------------

    # Trait property handlers ------------------------------------------------

    def _get_active(self):
        return self._active

    def _set_active(self, value):
        if value:
            self.start()
        else:
            self.stop()


@provides(IEventTimer)
class MEventTimer(HasTraits):
    """ Mixin for event timer classes.

    Other code can listen to the `timeout` event using standard traits
    listeners.
    """

    # IEventTimer interface --------------------------------------------------

    #: A traits Event to fire when the callback happens.
    timeout = Event()

    # -------------------------------------------------------------------------
    # ITimer interface
    # -------------------------------------------------------------------------

    # ITimer Protected methods -----------------------------------------------

    def _perform(self):
        """ Fire the event. """
        self.timeout = True


@provides(ITimer)
class MCallbackTimer(HasTraits):
    """ Mixin for callback timer classes.
    """

    # ICallbackTimer interface -----------------------------------------------

    #: The callback to make.
    callback = Callable

    #: Positional arguments to give the callback.
    args = Tuple()

    #: Keyword arguments to give the callback.
    kwargs = Dict()

    # -------------------------------------------------------------------------
    # ITimer interface
    # -------------------------------------------------------------------------

    # ITimer Protected methods -----------------------------------------------

    def _perform(self):
        """ Perform the callback. """
        self.callback(*self.args, **self.kwargs)
