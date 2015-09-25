#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
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
#------------------------------------------------------------------------------

# Import the toolkit specific version.
from pyface.toolkit import toolkit_object
DoLaterTimer = toolkit_object('timer.do_later:DoLaterTimer')


def do_later(callable, *args, **kw_args):
    """ Does something 50 milliseconds from now.

    Parameters
    ----------
    callable : callable
        The callable to call in 50ms time.
    args, kwargs :
        Arguments to be passed through to the callable.
    """
    DoLaterTimer(50, callable, args, kw_args)


def do_after(interval, callable, *args, **kw_args):
    """ Does something after some specified time interval.

    Parameters
    ----------
    interval : float
        The time interval to wait before calling.
    callable : callable
        The callable to call in 50ms time.
    args, kwargs :
        Arguments to be passed through to the callable.
    """
    DoLaterTimer(interval, callable, args, kw_args)
