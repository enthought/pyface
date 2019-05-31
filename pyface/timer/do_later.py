# Copyright (c) 2005-18, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought util package component>

from pyface.timer.timer import CallbackTimer, Timer


class DoLaterTimer(Timer):
    """ Performs a callback once at a later time.

    This is not used by the `do_later` functions and is only provided for
    backwards compatibility of the API.
    """

    #: The perform the callback once.
    repeat = 1

    def __init__(self, interval, callable, args, kw_args):
        # Adapt the old DoLaterTimer initializer to the Timer initializer.
        super(DoLaterTimer, self).__init__(interval, callable, *args, **kw_args)


def do_later(callable, *args, **kwargs):
    """ Does something 50 milliseconds from now.

    Parameters
    ----------
    callable : callable
        The callable to call in 50ms time.
    *args, **kwargs :
        Arguments to be passed through to the callable.
    """
    return CallbackTimer.single_shot(
        interval=0.05,
        callback=callable,
        args=args,
        kwargs=kwargs,
    )


def do_after(interval, callable, *args, **kwargs):
    """ Does something after some specified time interval.

    Parameters
    ----------
    interval : float
        The time interval in milliseconds to wait before calling.
    callable : callable
        The callable to call.
    *args, **kwargs :
        Arguments to be passed through to the callable.
    """
    return CallbackTimer.single_shot(
        interval=interval / 1000.0,
        callback=callable,
        args=args,
        kwargs=kwargs,
    )
