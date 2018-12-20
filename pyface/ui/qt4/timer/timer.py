# Copyright (c) 2007, Riverbank Computing Limited
# Copyright (c) 2018, Enthought Inc
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license.  However, when used with the GPL version of PyQt the additional
# terms described in the PyQt GPL exception also apply

from traits.api import Instance

from pyface.qt.QtCore import QTimer
from pyface.timer.i_timer import BaseTimer


class PyfaceTimer(BaseTimer):
    """ Abstract base class for Qt toolkit timers. """

    #: The QTimer for the PyfaceTimer.
    _timer = Instance(QTimer, (), allow_none=False)

    def __init__(self, **traits):
        traits.setdefault('_timer', QTimer())
        super(PyfaceTimer, self).__init__(**traits)
        self._timer.timeout.connect(self.perform)

    def _start(self):
        self._timer.start(int(self.interval * 1000))

    def _stop(self):
        self._timer.stop()
