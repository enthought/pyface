======
Timers
======

Pyface provides a unified interface for toolkit timers.  There are two levels
to this inferface: a simple functional interface for simple single-shot
deferred callbacks, and a more complex interface for application-level timers
such as heartbeats and periodic monitors.

It is worth remembering that timers are only as accurate as the underlying
toolkit and operating system permit; in particular the toolkits usually
guarantee that they will be called no sooner than any specified delay, but
they may be called much later (eg. worst case, if an operating system sleep
occurs between a timer being set and being run, the delay can be arbitrarily
long).

Functional Interface
====================

The basic functional interface is found in :py:mod:`pyface.timer.do_later`.
This provides two functions :py:func:`~pyface.timer.do_later.do_later` and
:py:func:`~pyface.timer.do_later.do_after`.  These two functions behave in
essentially the same way, expecting a callback with arguments to be performed
once at some later time, the difference being that
:py:mod:`~pyface.timer.do_later.do_later` hard-codes the time to be 50
milliseconds.

.. code-block:: python

    import datetime
    from pyface.timer.api import do_after, do_later

    DEFAULT_DELTA = datetime.timedelta(milliseconds=50)

    def report_time(time_started, expected_delay=DEFAULT_DELTA):
        time_now = datetime.datetime.utcnow()

        print("Time started: {}".format(time_started))
        print("Time now: {}".format(time_now))
        print("Expected delay: {}".format(expected_delay))
        print("Actual delay:   {}".format(time_now - time_started))
    
    now = datetime.utcnow()
    delay=datetime.timedelta(seconds=10)
    do_after(10 * 1000, report_time, now, expected_delay=delay)
    
    now = datetime.utcnow()
    do_later(report_time, now)

.. note::
    For historical reasons, the :py:mod:`pyface.timer.do_later` API expects
    times to be specified in milliseconds instead of seconds.

An alternative functional interface with similar capabilties is available via
the :py:meth:`pyface.timer.timer.CallbackTimer.single_shot` class method.


Timer Classes
=============

For more complex needs, the :py:mod:`pyface.timer.timer` module provides a
base timer class and several convenience subclasses for common use cases.


PyfaceTimer
-----------

The :py:class:`pyface.timer.timer.PyfaceTimer` is a base class that can be
subclassed by providing a :py:meth:`~pyface.timer.timer.PyfaceTimer._perform`
method.

.. code-block:: python

    import datetime
    from pyface.timer.api import PyfaceTimer

    class CustomTimer(PyfaceTimer):

        def _perform(self):
            print("The time is {}".format(datetime.datetime.now()))

:py:class:`~pyface.timer.timer.PyfaceTimer` and its subclasses provide a
number of traits and methods to control the frequency and number of times the
timer performs its action.  The most important of these is
:py:attr:`~pyface.timer.timer.PyfaceTimer.interval` which determines the time
until the first call and between any subsequent calls.

Timers are explicitly started by explicitly calling their
:py:meth:`~pyface.timer.timer.PyfaceTimer.start` method, or by setting their
:py:attr:`~pyface.timer.timer.PyfaceTimer.active` trait to ``True``. By
default, the timer will repeat indefinately until it is explicitly
halted via :py:meth:`~pyface.timer.timer.PyfaceTimer.stop` or setting
:py:attr:`~pyface.timer.timer.PyfaceTimer.active` trait to ``False`` (or by the
application shutting down).

Rather than controlling the active state of the timer explicitly, the number of
invocations of the :py:meth:`~pyface.timer.timer.PyfaceTimer.perfom` method can
be controlled either via setting the
:py:attr:`~pyface.timer.timer.PyfaceTimer.repeat` trait to an explicit number
of times to repeat and/or setting the
:py:attr:`~pyface.timer.timer.PyfaceTimer.expire` trait to a maximum number of
seconds for the timer to run (which could potentially mean that the timer never
gets performed).

For example, a timer which repeats every 0.5 seconds and runs no more than 10
times and for no longer than 10 seconds can be started like this -

.. code-block:: python

    timer = CustomTimer(interval=0.5, repeat=10, expire=10)
    timer.start()

:py:class:`~pyface.timer.timer.PyfaceTimer` also provides two convenience class
methods for creating and starting a timer in one line.  The above example
could instead be written as -

.. code-block:: python

    timer = CustomTimer.timer(interval=0.5, repeat=10, expire=10)
    
For the common case of a "single-shot" timer that is only performed once,
there is the :py:meth:`~pyface.timer.timer.PyfaceTimer.single_shot` class
method that creates a timer that will be called once after the specified
interval -

.. code-block:: python

    CustomTimer.single_shot(interval=0.5)

.. note::

    To avoid the Python timer objects being garbage-collected prematurely,
    references are kept to all active timers by Pyface.  This means that you
    can safely create timers without having to explicitly hold a long-term
    reference to them if you do not need it for other reasons.


CallbackTimer
-------------

Rather than subclassing :py:class:`~pyface.timer.timer.PyfaceTimer` for every
timer that you want, it is often enough to supply a callback function (possibly
with arguments) to be called by the timer.  Pyface provides the
:py:class:`~pyface.timer.timer.CallbackTimer` class for this purpose.

This class is meant to be directly instantiated, providing at a minimum a
callable value for the :py:attr:`~pyface.timer.timer.CallbackTimer.callback`
trait, along with an optional tuple of
:py:attr:`~pyface.timer.timer.CallbackTimer.args` and/or optional dict of
:py:attr:`~pyface.timer.timer.CallbackTimer.kwargs`.

.. code-block:: python

    from pyface.timer.api import CallbackTimer
    
    def print_time():
        print("The time is {}".format(datetime.datetime.now()))

    CallbackTimer.timer(callback=print_time, interval=0.5, expire=60)


EventTimer
----------

Another common use case is that you want a Traits Event to be fired
periodically or at some future time.  This permits many possible listeners
to be called from the same timer, and have them be turned on and turned off
dynamically, if desired, via
`Traits' observe <https://docs.enthought.com/traits/traits_user_manual/notification.html>`_
(note that observe listeners are required to take a single event argument).
The :py:class:`~pyface.timer.timer.EventTimer` provides this functionality via
its :py:class:`~pyface.timer.timer.EventTimer.timeout` event trait.

.. code-block:: python

    from pyface.timer.api import EventTimer

    def print_time(event):
        print("The time is {}".format(datetime.datetime.now()))

    timer = EventTimer(interval=0.5, expire=60)
    timer.observe(print_time, 'timeout')

    timer.start()

The :py:class:`~pyface.timer.timer.EventTimer` class is particularly suited to
be used as an application "heartbeat" that arbitrary code can hook into to be
run periodically without having to create its own timer.

Deprecated Classes
------------------

Pyface also provides a deprecated :py:class:`~pyface.timer.timer.Timer`
class for backwards compatability.  This class shouldn't be used in new code.