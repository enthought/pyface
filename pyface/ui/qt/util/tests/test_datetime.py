# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Utility functions for handling Qt dates and times. """

import datetime
import unittest

from pyface.qt.QtCore import QTime

from ..datetime import pytime_to_qtime, qtime_to_pytime


class TestTimeConversion(unittest.TestCase):

    def test_pytime_to_qtime(self):
        pytime = datetime.time(9, 8, 7, 123456)

        qtime = pytime_to_qtime(pytime)

        self.assertEqual(qtime.hour(), 9)
        self.assertEqual(qtime.minute(), 8)
        self.assertEqual(qtime.second(), 7)
        self.assertEqual(qtime.msec(), 123)

    def test_qtime_to_pytime(self):
        qtime = QTime(9, 8, 7, 123)

        pytime = qtime_to_pytime(qtime)

        self.assertEqual(pytime.hour, 9)
        self.assertEqual(pytime.minute, 8)
        self.assertEqual(pytime.second, 7)
        self.assertEqual(pytime.microsecond, 123000)
