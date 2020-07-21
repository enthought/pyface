from unittest import TestCase

from ..color_parser import (
    ColorParseError, channels_to_ints, color_table, ints_to_channels,
    parse_functional, parse_hex, parse_name, parse_text,
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


class TestParseFunctional(TestCase):

    def test_4_tuple_normalized(self):
        space, channels = parse_functional('(0.4, 0.4, 0.0, 1.0)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_4_tuple_bytes(self):
        space, channels = parse_functional('(102, 102, 0, 255)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_4_tuple_no_comma(self):
        space, channels = parse_functional('(0.4 0.4 0.0 1.0)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_rgba_normalized(self):
        space, channels = parse_functional('rgba(0.4, 0.4, 0.0, 1.0)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_rgba_bytes(self):
        space, channels = parse_functional('rgba(102, 102, 0, 255)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_rgba_no_comma(self):
        space, channels = parse_functional('rgba(0.4 0.4 0.0 1.0)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_hsva_normalized(self):
        space, channels = parse_functional('hsva(0.4, 0.4, 0.0, 1.0)')
        self.assertEqual(space, 'hsva')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_hsva_bytes(self):
        space, channels = parse_functional('hsva(102, 102, 0, 255)')
        self.assertEqual(space, 'hsva')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_hlsa_normalized(self):
        space, channels = parse_functional('hlsa(0.4, 0.4, 0.0, 1.0)')
        self.assertEqual(space, 'hlsa')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_hlsa_bytes(self):
        space, channels = parse_functional('hlsa(102, 102, 0, 255)')
        self.assertEqual(space, 'hlsa')
        self.assertEqual(channels, (0.4, 0.4, 0.0, 1.0))

    def test_3_tuple_normalized(self):
        space, channels = parse_functional('(0.4, 0.4, 0.0)')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_3_tuple_bytes(self):
        space, channels = parse_functional('(102, 102, 0)')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_3_tuple_no_comma(self):
        space, channels = parse_functional('(0.4 0.4 0.0)')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_rgb_normalized(self):
        space, channels = parse_functional('rgb(0.4, 0.4, 0.0)')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_rgb_bytes(self):
        space, channels = parse_functional('rgb(102, 102, 0)')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_rgb_no_comma(self):
        space, channels = parse_functional('rgb(0.4 0.4 0.0)')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_hsv_normalized(self):
        space, channels = parse_functional('hsv(0.4, 0.4, 0.0)')
        self.assertEqual(space, 'hsv')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_hsv_bytes(self):
        space, channels = parse_functional('hsv(102, 102, 0)')
        self.assertEqual(space, 'hsv')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_hls_normalized(self):
        space, channels = parse_functional('hls(0.4, 0.4, 0.0)')
        self.assertEqual(space, 'hls')
        self.assertEqual(channels, (0.4, 0.4, 0.0))

    def test_hls_bytes(self):
        space, channels = parse_functional('hls(102, 102, 0)')
        self.assertEqual(space, 'hls')
        self.assertEqual(channels, (0.4, 0.4, 0.0))


class TestParseHex(TestCase):

    def test_hex_3(self):
        space, channels = parse_hex('#06c')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.0, 0.4, 0.8))

    def test_hex_4(self):
        space, channels = parse_hex('#06cf')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.0, 0.4, 0.8, 1.0))

    def test_hex_6(self):
        space, channels = parse_hex('#0066cc')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.0, 0.4, 0.8))

    def test_hex_8(self):
        space, channels = parse_hex('#0066ccff')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.0, 0.4, 0.8, 1.0))

    def test_hex_12(self):
        space, channels = parse_hex('#00006666cccc')
        self.assertEqual(space, 'rgb')
        self.assertEqual(channels, (0.0, 0.4, 0.8))

    def test_hex_16(self):
        space, channels = parse_hex('#00006666ccccffff')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.0, 0.4, 0.8, 1.0))

    def test_hex_bad(self):
        result = parse_hex('#0c')
        self.assertIsNone(result)


class TestParseName(TestCase):

    def test_names(self):
        for name, value in color_table.items():
            with self.subTest(color=name):
                space, channels = parse_name(name)
                self.assertEqual(space, 'rgba')
                self.assertEqual(channels, value)

    def test_name_space(self):
        space, channels = parse_name('rebecca purple')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.2, 0.6, 1.0))

    def test_name_capitals(self):
        space, channels = parse_name('RebeccaPurple')
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

    def test_functional(self):
        space, channels = parse_text('rgba(0.4, 0.2, 0.6, 1.0)')
        self.assertEqual(space, 'rgba')
        self.assertEqual(channels, (0.4, 0.2, 0.6, 1.0))

    def test_error(self):
        with self.assertRaises(ColorParseError):
            parse_text('invalidcolorname')
