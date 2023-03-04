# (C) Copyright 2007 Riverbank Computing Limited
# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance

from pyface.qt.QtCore import QTimer
from pyface.timer.i_timer import BaseTimer


class PyfaceTimer(BaseTimer):
    """ Abstract base class for Qt toolkit timers. """

    #: The QTimer for the PyfaceTimer.
    _timer = Instance(QTimer, (), allow_none=False)

    def __init__(self, **traits):
        traits.setdefault("_timer", QTimer())
        super().__init__(**traits)
        self._timer.timeout.connect(self.perform)

    def _start(self):
        self._timer.start(int(self.interval * 1000))

    def _stop(self):
        self._timer.stop()
