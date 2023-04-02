# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""A `wx.Timer` subclass that invokes a specified callback periodically.
"""

import wx

from traits.api import Instance

from pyface.timer.i_timer import BaseTimer


class CallbackTimer(wx.Timer):
    def __init__(self, timer):
        super().__init__()
        self.timer = timer

    def Notify(self):
        self.timer.perform()
        wx.GetApp().Yield(True)


class PyfaceTimer(BaseTimer):
    """ Abstract base class for Wx toolkit timers. """

    #: The wx.Timer for the PyfaceTimer.
    _timer = Instance(wx.Timer)

    def _start(self):
        self._timer.Start(int(self.interval * 1000))

    def _stop(self):
        self._timer.Stop()

    def __timer_default(self):
        return CallbackTimer(self)
