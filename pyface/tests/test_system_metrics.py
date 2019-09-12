from __future__ import absolute_import

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
