# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase

from pyface.color import Color
from pyface.color_tuple import ColorTuple


class TestColorTuple(TestCase):

    def assert_tuple_almost_equal(self, tuple_1, tuple_2):
        self.assertEqual(len(tuple_1), len(tuple_2))

        for x, y in zip(tuple_1, tuple_2):
            self.assertAlmostEqual(x, y)

    def test_init(self):
        color = ColorTuple()
        self.assertEqual(color, (1.0, 1.0, 1.0, 1.0))

    def test_init_rgba(self):
        color = ColorTuple(0.4, 0.2, 0.6, 0.8)
        self.assertEqual(color, (0.4, 0.2, 0.6, 0.8))

    def test_init_rgb(self):
        color = ColorTuple(0.4, 0.2, 0.6)
        self.assertEqual(color, (0.4, 0.2, 0.6, 1.0))

    def test_init_r_g_b_a(self):
        color = ColorTuple(red=0.4, green=0.2, blue=0.6, alpha=0.8)
        self.assertEqual(color, (0.4, 0.2, 0.6, 0.8))

    def test_init_r_g_b(self):
        color = ColorTuple(red=0.4, green=0.2, blue=0.6)
        self.assertEqual(color, (0.4, 0.2, 0.6, 1.0))

    def test_from_str_name(self):
        color = ColorTuple.from_str('rebeccapurple')
        self.assertEqual(color, (0.4, 0.2, 0.6, 1.0))

    def test_from_str_hex(self):
        color = ColorTuple.from_str('#663399ff')
        self.assertEqual(color, (0.4, 0.2, 0.6, 1.0))

    def test_toolkit_round_trip(self):
        color = ColorTuple(0.4, 0.2, 0.6, 0.8)
        toolkit_color = color.to_toolkit()
        result = ColorTuple.from_toolkit(toolkit_color)
        self.assertEqual(result, color)

    def test_from_color(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color_tuple = ColorTuple.from_color(color)
        self.assertEqual(color_tuple, (0.4, 0.2, 0.6, 0.8))

    def test_hex(self):
        color = ColorTuple(0.4, 0.2, 0.6, 0.8)
        hex_value = color.hex()
        self.assertEqual(hex_value, "#663399CC")

    def test_hex_black(self):
        color = ColorTuple(0.0, 0.0, 0.0, 1.0)
        hex_value = color.hex()
        self.assertEqual(hex_value, "#000000FF")

    def test_str(self):
        color = ColorTuple(0.4, 0.2, 0.6, 0.8)
        result = str(color)
        self.assertEqual(result, "(0.4, 0.2, 0.6, 0.8)")

    def test_get_rgb(self):
        color = ColorTuple(0.4, 0.2, 0.6, 0.8)
        self.assertEqual(color.rgb, (0.4, 0.2, 0.6))

    def test_get_hsv(self):
        color = ColorTuple(0.48, 0.6, 0.528, 0.8)
        self.assert_tuple_almost_equal(color.hsv, (0.4, 0.2, 0.6))

    def test_get_hsva(self):
        color = ColorTuple(0.48, 0.6, 0.528, 0.8)
        self.assert_tuple_almost_equal(color.hsva, (0.4, 0.2, 0.6, 0.8))

    def test_get_hls(self):
        color = ColorTuple(0.08, 0.32, 0.176, 0.8)
        self.assert_tuple_almost_equal(color.hls, (0.4, 0.2, 0.6))

    def test_get_hlsa(self):
        color = ColorTuple(0.08, 0.32, 0.176, 0.8)
        self.assert_tuple_almost_equal(color.hlsa, (0.4, 0.2, 0.6, 0.8))

    def test_get_is_dark(self):
        color = ColorTuple(0.08, 0.32, 0.176, 0.8)
        self.assertTrue(color.is_dark)
