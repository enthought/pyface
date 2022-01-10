# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""

API for the ``pyface.timer`` subpackage.

- :func:`~.do_later`
- :func:`~.do_after`
- :class:`~.DoLaterTimer`
- :class:`~.CallbackTimer`
- :class:`~.EventTimer`
- :class:`~.Timer`

Interfaces
----------
- :class:`~.ICallbackTimer`
- :class:`~.IEventTimer`
- :class:`~.ITimer`

"""

from .do_later import do_later, do_after, DoLaterTimer
from .i_timer import ICallbackTimer, IEventTimer, ITimer
from .timer import CallbackTimer, EventTimer, Timer
