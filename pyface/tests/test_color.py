from unittest import TestCase

from traits.api import DefaultValue, TraitError
from traits.testing.optional_dependencies import numpy as np, requires_numpy
from traits.testing.unittest_tools import UnittestTools

from ..color import (
    Color, ColorParseError, PyfaceColor, channels_to_ints, color_table,
    ints_to_channels, parse_functional, parse_hex, parse_name, parse_text,
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

    def test_from_str_name(self):
        color = Color.from_str('rebeccapurple')
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 1.0))

    def test_from_str_hex(self):
        color = Color.from_str('#663399ff')
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 1.0))

    def test_from_str_functional(self):
        color = Color.from_str('rgba(0.4, 0.2, 0.6, 1.0)')
        self.assertEqual(color.rgba, (0.4, 0.2, 0.6, 1.0))

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


class TestPyfaceColor(TestCase):

    def test_init(self):
        trait = PyfaceColor()
        self.assertEqual(trait.default_value, (Color, (), {}))
        self.assertEqual(
            trait.default_value_type,
            DefaultValue.callable_and_args,
        )

    def test_init_str(self):
        trait = PyfaceColor("rebeccapurple")
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_color(self):
        trait = PyfaceColor(Color(rgba=(0.4, 0.2, 0.6, 1.0)))
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_tuple(self):
        trait = PyfaceColor((0.4, 0.2, 0.6, 1.0))
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_list(self):
        trait = PyfaceColor([0.4, 0.2, 0.6, 1.0])
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    @requires_numpy
    def test_init_array(self):
        trait = PyfaceColor(np.array([0.4, 0.2, 0.6, 1.0]))
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    @requires_numpy
    def test_init_array_structured_dtype(self):
        """ Test if "typical" RGBA structured array value works. """
        arr = np.array(
            [(0.4, 0.2, 0.6, 1.0)],
            dtype=np.dtype([
                ('red', float),
                ('green', float),
                ('blue', float),
                ('alpha', float),
            ]),
        )
        trait = PyfaceColor(arr[0])
        self.assertEqual(
            trait.default_value,
            (Color, (), {'rgba': (0.4, 0.2, 0.6, 1.0)})
        )

    def test_init_invalid(self):
        with self.assertRaises(TraitError):
            PyfaceColor((0.4, 0.2))

    def test_validate_color(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 1.0))
        trait = PyfaceColor()
        validated = trait.validate(None, None, color)
        self.assertIs(
            validated, color
        )

    def test_validate_tuple(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        trait = PyfaceColor()
        validated = trait.validate(None, None, (0.4, 0.2, 0.6, 0.8))
        self.assertEqual(
            validated, color
        )

    def test_validate_list(self):
        color = Color(rgba=(0.4, 0.2, 0.6, 0.8))
        trait = PyfaceColor()
        validated = trait.validate(None, None, [0.4, 0.2, 0.6, 0.8])
        self.assertEqual(
            validated, color
        )

    def test_info(self):
        trait = PyfaceColor()
        self.assertIsInstance(trait.info(), str)
