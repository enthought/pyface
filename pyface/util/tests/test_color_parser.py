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

from ..color_parser import (
    ColorParseError, color_table, parse_text, _parse_hex, _parse_name
)


class TestParseHex(TestCase):

    def test_hex_3(self):
        space, channels = _parse_hex('#06c')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.0, 0.4, 0.8))

    def test_hex_4(self):
        space, channels = _parse_hex('#06cf')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.0, 0.4, 0.8, 1.0))

    def test_hex_6(self):
        space, channels = _parse_hex('#0066cc')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.0, 0.4, 0.8))

    def test_hex_8(self):
        space, channels = _parse_hex('#0066ccff')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.0, 0.4, 0.8, 1.0))

    def test_hex_12(self):
        space, channels = _parse_hex('#00006666cccc')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.0, 0.4, 0.8))

    def test_hex_16(self):
        space, channels = _parse_hex('#00006666ccccffff')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.0, 0.4, 0.8, 1.0))

    def test_hex_bad(self):
        result = _parse_hex('#0c')
        self.assertIsNone(result)


class TestParseName(TestCase):

    def test_names(self):
        for name, value in color_table.items():
            with self.subTest(color=name):
                space, channels = _parse_name(name)
                self.assertEqual(space, 'rgba')
                self.assertEqual(channels, value)

    def test_name_space(self):
        space, channels = _parse_name('rebecca purple')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.2, 0.6, 1.0))

    def test_name_capitals(self):
        space, channels = _parse_name('RebeccaPurple')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.2, 0.6, 1.0))


class TestParseText(TestCase):

    def test_name(self):
        space, channels = parse_text('rebeccapurple')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.2, 0.6, 1.0))

    def test_hex(self):
        space, channels = parse_text('#663399ff')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.2, 0.6, 1.0))

    def test_error(self):
        with self.assertRaises(ColorParseError):
            parse_text('invalidcolorname')
