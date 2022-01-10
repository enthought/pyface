# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from ..system_metrics import SystemMetrics


class TestSystemMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = SystemMetrics()

    def test_width(self):
        width = self.metrics.screen_width
        self.assertGreaterEqual(width, 0)

    def test_height(self):
        height = self.metrics.screen_height
        self.assertGreaterEqual(height, 0)

    def test_background_color(self):
        color = self.metrics.dialog_background_color
        self.assertIn(len(color), [3, 4])
        self.assertTrue(all(0 <= channel <= 1 for channel in color))
