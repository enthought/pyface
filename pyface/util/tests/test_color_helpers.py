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

from pyface.util.color_helpers import (
    channels_to_ints, ints_to_channels, is_dark, relative_luminance
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
