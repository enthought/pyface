# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase, skipIf

try:
    import numpy as np
except ImportError:
    np = None

from pyface.util.color_helpers import (
    channels_to_ints, ints_to_channels, is_dark, relative_luminance,
    int_to_color_tuple, sequence_to_rgba_tuple
)


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


class TestRelativeLuminance(TestCase):

    def test_white(self):
        rgb = (1.0, 1.0, 1.0)
        result = relative_luminance(rgb)
        self.assertEqual(result, 1.0)

    def test_black(self):
        rgb = (0.0, 0.0, 0.0)
        result = relative_luminance(rgb)
        self.assertEqual(result, 0.0)

    def test_red(self):
        rgb = (1.0, 0.0, 0.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.2126)

    def test_green(self):
        rgb = (0.0, 1.0, 0.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.7152)

    def test_blue(self):
        rgb = (0.0, 0.0, 1.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.0722)

    def test_yellow(self):
        rgb = (1.0, 1.0, 0.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.2126 + 0.7152)

    def test_cyan(self):
        rgb = (0.0, 1.0, 1.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.7152 + 0.0722)

    def test_magenta(self):
        rgb = (1.0, 0.0, 1.0)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.2126 + 0.0722)

    def test_dark_grey(self):
        rgb = (0.01, 0.01, 0.01)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, 0.01/12.92)

    def test_medium_grey(self):
        rgb = (0.5, 0.5, 0.5)
        result = relative_luminance(rgb)
        self.assertAlmostEqual(result, (0.555/1.055)**2.4)


class TestIsDark(TestCase):

    def test_white(self):
        rgb = (1.0, 1.0, 1.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_black(self):
        rgb = (0.0, 0.0, 0.0)
        result = is_dark(rgb)
        self.assertTrue(result)

    def test_red(self):
        rgb = (1.0, 0.0, 0.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_green(self):
        rgb = (0.0, 1.0, 0.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_blue(self):
        rgb = (0.0, 0.0, 1.0)
        result = is_dark(rgb)
        self.assertTrue(result)

    def test_yellow(self):
        rgb = (1.0, 1.0, 0.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_cyan(self):
        rgb = (0.0, 1.0, 1.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_magenta(self):
        rgb = (1.0, 0.0, 1.0)
        result = is_dark(rgb)
        self.assertFalse(result)

    def test_dark_grey(self):
        rgb = (0.01, 0.01, 0.01)
        result = is_dark(rgb)
        self.assertTrue(result)

    def test_medium_grey(self):
        rgb = (0.5, 0.5, 0.5)
        result = is_dark(rgb)
        self.assertFalse(result)


class TestIntToColorTuple(TestCase):

    def test_good(self):
        cases = {
            0x000000: (0.0, 0.0, 0.0),
            0xffffff: (1.0, 1.0, 1.0),
            0x663399: (0.4, 0.2, 0.6),
        }
        for value, result in cases.items():
            with self.subTest(value=value):
                self.assertEqual(int_to_color_tuple(value), result)

    def test_bad(self):
        cases = [-1, 0x1000000]
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    int_to_color_tuple(value)


class TestSequenceToRGBATuple(TestCase):

    def test_good(self):
        cases = [
            (0.4, 0.2, 0.6, 1.0),
            [0.4, 0.2, 0.6, 1.0],
            (0x66, 0x33, 0x99, 0xff),
            [0x66, 0x33, 0x99, 0xff],
            (0.4, 0.2, 0.6),
            [0.4, 0.2, 0.6],
            (0x66, 0x33, 0x99),
            [0x66, 0x33, 0x99],
        ]

        for value in cases:
            with self.subTest(value=value):
                self.assertEqual(
                    sequence_to_rgba_tuple(value),
                    (0.4, 0.2, 0.6, 1.0),
                )

    @skipIf(np is None, "NumPy is needed for test")
    def test_good_numpy(self):
        rgba_float_dtype = np.dtype([
            ('red', "float64"),
            ('green', "float64"),
            ('blue', "float64"),
            ('alpha', "float64"),
        ])
        rgba_uint8_dtype = np.dtype([
            ('red', "uint8"),
            ('green', "uint8"),
            ('blue', "uint8"),
            ('alpha', "uint8"),
        ])
        rgb_float_dtype = np.dtype([
            ('red', "float64"),
            ('green', "float64"),
            ('blue', "float64"),
        ])
        rgb_uint8_dtype = np.dtype([
            ('red', "uint8"),
            ('green', "uint8"),
            ('blue', "uint8"),
        ])

        cases = [
            np.array([0.4, 0.2, 0.6, 1.0]),
            np.array([(0.4, 0.2, 0.6, 1.0)], dtype=rgba_float_dtype)[0],
            np.array([0x66, 0x33, 0x99, 0xff], dtype='uint8'),
            np.array([(0x66, 0x33, 0x99, 0xff)], dtype=rgba_uint8_dtype)[0],
            np.array([0.4, 0.2, 0.6]),
            np.array([(0.4, 0.2, 0.6)], dtype=rgb_float_dtype)[0],
            np.array([0x66, 0x33, 0x99], dtype='uint8'),
            np.array([(0x66, 0x33, 0x99)], dtype=rgb_uint8_dtype)[0],
        ]

        for value in cases:
            with self.subTest(value=value):
                self.assertEqual(
                    sequence_to_rgba_tuple(value),
                    (0.4, 0.2, 0.6, 1.0),
                )

    def test_bad(self):
        cases = [
            (0.4, 0.2),
            (0.4, 0.2, 0.3, 1.0, 1.0),
            (0.0, 1.00001, 0.9, 1.0),
            (0.0, -0.00001, 0.9, 1.0),
            (0, -1, 250, 255),
        ]
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    sequence_to_rgba_tuple(value)
