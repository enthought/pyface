# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase

from traits.testing.unittest_tools import UnittestTools

from pyface.color import Color, channels_to_ints, ints_to_channels


class TestChannelConversion(TestCase):

    def test_ints_to_channels(self):
        values = (102, 102, 0, 255)
        channels = ints_to_channels(values)
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_ints_to_channels_maximum(self):
        values = (6, 6, 0, 15)
        channels = ints_to_channels(values, maximum=15)
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_channels_to_ints(self):
        channels = (0.4, 0.4, 0.0, 1.0)
        values = channels_to_ints(channels)
        self.assertEqual(values, (102, 102, 0, 255))

    def test_channels_to_ints_maximum(self):
        channels = (0.4, 0.4, 0.0, 1.0)
        values = channels_to_ints(channels, maximum=15)
        self.assertEqual(values, (6, 6, 0, 15))

    def test_round_trip(self):
        """ Test to assert stability of values through round-trips """
        for value in range(256):
            with self.subTest(int=value):
                result = channels_to_ints(ints_to_channels([value]))
                self.assertEqual(result, (value,))

    def test_round_trip_maximum(self):
        """ Test to assert stability of values through round-trips """
        for value in range(65536):
            with self.subTest(int=value):
                result = channels_to_ints(
                    ints_to_channels(
                        [value],
                        maximum=65535,
                    ),
                    maximum=65535,
                )
                self.assertEqual(result, (value,))



class TestColor(UnittestTools, TestCase):

    def test_init(self):
        color = Color()
        self.assertEqual(color.rgba, (1.0, 1.0, 1.0, 1.0))

    def test_init_rgba(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 0.8))

    def test_init_rgb(self):
        color = Color(rgb=(0.4, 0.2, 0.6))
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 1.0))

    def test_init_r_g_b_a(self):
        color = Color(red=0.4, green=0.2, blue=0.6, alpha=0.8)
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 0.8))

    def test_init_r_g_b(self):
        color = Color(red=0.4, green=0.2, blue=0.6)
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 1.0))

    def test_init_hsva(self):
        color = Color(hsva=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.rgba, (0.48, 0.6, 0.528, 0.8))

    def test_init_hsv(self):
        color = Color(hsv=(0.4, 0.2, 0.6))
        self.assertEqual(color.rgba, (0.48, 0.6, 0.528, 1.0))

    def test_init_hlsa(self):
        color = Color(hlsa=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(
            color.rgba,
            (0.07999999999999996, 0.32000000000000006, 0.17600000000000007, 0.8)  # noqa: E501
        )

    def test_init_hls(self):
        color = Color(hls=(0.4, 0.2, 0.6))
        self.assertEqual(
            color.rgba,
            (0.07999999999999996, 0.32000000000000006, 0.17600000000000007, 1.0)  # noqa: E501
        )

    def test_toolkit_round_trip(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        toolkit_color = color.to_toolkit()
        result = Color.from_toolkit(toolkit_color)
        self.assertEqual(result.rgba, (0.4, 0.2, 0.6, 0.8))

    def test_hex(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        hex_value = color.hex()
        self.assertEqual(hex_value, "#663399CC")

    def test_hex_black(self):
        color = Color(rgba=(0.0, 0.0, 0.0, 1.0))
        hex_value = color.hex()
        self.assertEqual(hex_value, "#000000FF")

    def test_eq(self):
        color_1 = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color_2 = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertTrue(color_1 == color_2)
        self.assertFalse(color_1 != color_2)

    def test_eq_not_eequal(self):
        color_1 = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color_2 = Color(rgba=(0.4, 0.4, 0.6, 0.8))
        self.assertTrue(color_1 != color_2)
        self.assertFalse(color_1 == color_2)

    def test_eq_other(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertFalse(color == 1)
        self.assertTrue(color != 1)

    def test_not_eq(self):
        color_1 = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color_2 = Color(rgba=(0.0, 0.0, 0.0, 1.0))
        self.assertTrue(color_1 != color_2)
        self.assertFalse(color_1 == color_2)

    def test_str(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        result = str(color)
        self.assertEqual(result, "(0.4, 0.2, 0.6, 0.8)")

    def test_repr(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        result = repr(color)
        self.assertEqual(result, "Color(rgba=(0.4, 0.2, 0.6, 0.8))")

    def test_get_red(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.red, 0.4)

    def test_set_red(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color.red = 1.0
        self.assertEqual(color.rgba, (1.0, 0.2, 0.6, 0.8))

    def test_get_green(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.green, 0.2)

    def test_set_green(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color.green = 1.0
        self.assertEqual(color.rgba, (0.4, 1.0, 0.6, 0.8))

    def test_get_blue(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.blue, 0.6)

    def test_set_blue(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color.blue = 1.0
        self.assertEqual(color.rgba, (0.4, 0.2, 1.0, 0.8))

    def test_get_alpha(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.alpha, 0.8)

    def test_set_alpha(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color.alpha = 1.0
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 1.0))

    def test_get_rgb(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        self.assertEqual(color.rgb, (0.4, 0.2, 0.6))

    def test_set_rgb(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        color.rgb = (0.6, 0.8, 0.4)
        self.assertEqual(color.rgba, (0.6, 0.8, 0.4, 0.8))

    def test_get_hsv(self):
        color = Color(rgba=(0.48, 0.6, 0.528, 0.8))
        self.assertEqual(color.hsv, (0.4000000000000001, 0.2, 0.6))

    def test_set_hsv(self):
        color = Color()
        color.hsv = (0.4, 0.2, 0.6)
        self.assertEqual(color.rgba, (0.48, 0.6, 0.528, 1.0))

    def test_get_hsva(self):
        color = Color(rgba=(0.48, 0.6, 0.528, 0.8))
        self.assertEqual(color.hsva, (0.4000000000000001, 0.2, 0.6, 0.8))

    def test_set_hsva(self):
        color = Color()
        color.hsva = (0.4, 0.2, 0.6, 0.8)
        self.assertEqual(color.rgba, (0.48, 0.6, 0.528, 0.8))

    def test_get_hls(self):
        color = Color(rgba=(0.08, 0.32, 0.176, 0.8))
        self.assertEqual(
            color.hls,
            (0.39999999999999997, 0.2, 0.6)
        )

    def test_set_hls(self):
        color = Color()
        color.hls = (0.4, 0.2, 0.6)
        self.assertEqual(
            color.rgba,
            (0.07999999999999996, 0.32000000000000006, 0.17600000000000007, 1)
        )

    def test_get_hlsa(self):
        color = Color(rgba=(0.08, 0.32, 0.176, 0.8))
        self.assertEqual(
            color.hlsa,
            (0.39999999999999997, 0.2, 0.6, 0.8),
        )

    def test_set_hlsa(self):
        color = Color()
        color.hlsa = (0.4, 0.2, 0.6, 0.8)
        self.assertEqual(
            color.rgba,
            (0.07999999999999996, 0.32000000000000006, 0.17600000000000007, 0.8)  # noqa: E501
        )
