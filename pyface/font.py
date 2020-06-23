# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Toolkit-independent font utilities.

Pyface fonts are intended to be generic, but able to be mapped fairly well
to most backend toolkit font descriptions.  In most cases we can describe
fonts along the common dimensions that are used by CSS, Wx, and Qt.  However
when it comes to actually working with a font, the toolkit needs to take the
description and produce something that is as close as possible to the
specification, but within the constraints of the toolkit, operating system
and available fonts on the machine where this is being executed.

Font Properties
---------------

The properties that fonts have are:

Font Family
    A list of font family names in order of preference, such as "Helvetica"
    or "Comic Sans".  There are several generic font family names that can
    be used as fall-backs in case all preferred fonts are unavailable.  In
    the case of a font that has been selected by the toolkit this list will
    have one value which is the actual font family name.

Weight
    How thick or dark the font glyphs are.  These can be given as a number
    from 1 (lightest) to 999 (darkest), but are typically specified by a
    multiple of 100 from 100 to 900, with a number of synonyms such as 'light'
    and 'bold' available for those values.

Stretch
    The amount of horizontal compression or expansion to apply to the glyphs.
    These can be given as a number from 1 (most compressed) to 999 (most
    expanded), with a number of synonyms such as 'condensed' and 'expanded'
    available for those values.

Style
    This selects either 'oblique' or 'italic' variants typefaces of the given
    font family.  If neither is wanted, the value is 'normal'.

Size
    The overall size of the glyphs. This can be expressed either as the
    numeric size in points, or as a string such as "small" or "large".

Variants
    A set of additional font style specifiers, such as "small-caps",
    "strikethrough", "underline" or "overline", where supported by the
    underlying toolkit.

Text Description
----------------

Frequently it is useful to specify a font by a descriptive string (or supply
such a description to the user).  For these we follow the conventions in CSS
where fonts are specfied by a string which specifies the weight, stretch,
style and variants by text synonyms (in any order), followed by size in points
and font family preferences (quoted if not a single word) and separated by
commas.  Where the value is "normal" it can be omitted from the description.

For example::

    'italic bold 14pt Helvetica, Arial, sans-serif'
    '36pt "Comic Sans"'

When converting numeric values to string synonyms for display, the nearest
value will be chosen.  This may mean that text descriptions may not be
idempotent when run through font selection multiple times.

Font Specificiation Class
-------------------------

The Pyface Font class is a HasStrictTraits class which specifies a requested
font.  It has traits for all of the font properties, plus additional utility
methods that produce modifed versions of the font.

It also has methods that convert the Font class to and from a toolkit Font
class.

"""
import re

from traits.api import (
    BaseCFloat, DefaultValue, Enum, HasStrictTraits, CList, Map, CSet, Str,
    TraitError, TraitType
)
from traits.trait_type import NoDefaultSpecified

weights = {str(i): i for i in range(100, 1001, 100)}

# Note: we don't support 'medium' as an alias for weight 500 because it
# conflicts with the usage of 'medium' as an alias for a 12pt font in the CSS
# specification for font attributes.
weights.update({
    'thin': 100,
    'extra-light': 200,
    'ultra-light': 200,
    'light': 300,
    'normal': 400,
    'regular': 400,
    'book': 400,
    'semibold': 600,
    'demibold': 600,
    'demi': 600,
    'bold': 700,
    'extra-bold': 800,
    'ultra-bold': 800,
    'black': 900,
    'heavy': 900,
    'extra-heavy': 1000,
})

stretches = {
    'ultra-condensed': 100,
    'ultracondensed': 100,
    'extra-condensed': 200,
    'extracondensed': 200,
    'condensed': 300,
    'semi-condensed': 400,
    'semicondensed': 400,
    'normal': 500,
    'semi-expanded': 600,
    'semiexpanded': 600,
    'expanded': 700,
    'extra-expanded': 800,
    'extraexpanded': 800,
    'ultra-expanded': 900,
    'ultraexpanded': 900,
}

sizes = {
    'xx-small': 7.0,
    'x-small': 9.0,
    'small': 10.0,
    'medium': 12.0,
    'large': 14.0,
    'x-large': 18.0,
    'xx-large': 20.0,
}

styles = ['normal', 'italic', 'oblique']

variants = ['small-caps', 'underline', 'strikethrough', 'overline']

#: A trait for font families.
FontFamily = CList(Str, ['default'])

#: A trait for font weights.
FontWeight = Map(weights, default_value='normal')

#: A trait for font stretch values.
FontStretch = Map(stretches, default_value='normal')

#: A trait for font styles.
FontStyle = Enum(styles)

#: A trait for font variant properties.
FontVariants = CSet(Enum(variants))


class FontSize(BaseCFloat):
    """ Trait type for font sizes.

    The is a CFloat trait which also allows values which are keys of the
    size dictionary, and also ignores trailing 'pt' annotation in string
    values.  The value stored is a float.
    """

    #: The default value for the trait.
    default_value = 12.0

    def __init__(self, default_value=NoDefaultSpecified, **metadata):
        if default_value != NoDefaultSpecified:
            default_value = self.validate(None, None, default_value)
        super().__init__(default_value, **metadata)

    def validate(self, object, name, value):
        if isinstance(value, str) and value.endswith('pt'):
            value = value[:-2]
        value = sizes.get(value, value)
        value = super().validate(object, name, value)
        if value <= 0:
            self.error(object, name, value)
        return value

    def info(self):
        info = (
            "a positive float, a value that can convert to a positive float, "
        )
        info += ', '.join(repr(key) for key in sizes)
        info += (
            " or a string with a positive float value followed by 'pt'"
        )
        return info


font_tokens = [
    r'(?P<SIZE>\d+\.?\d*pt)',
    r'(?P<NUMBER>\d+\.?\d*)',
    r'(?P<NAME>[a-zA-Z\-]+)',
    r'(?P<QUOTED_NAME>"[^"]+"|\'[^\']+\')',
    r'(?P<COMMA>,)',
    r'(?P<WHITESPACE>\s+)',
    r'(?P<MISMATCH>.)',
]
token_re = re.compile('|'.join(font_tokens))


class FontParseError(ValueError):
    pass


parser_synonyms = {
    'slant': 'oblique'
}


def parse_font_description(description):
    """ An extremely relaxed parser for font descriptions.

    This is designed to accept most reasonable human-written text font
    descriptions and produce an acceptable set of parameters suitable as
    trait values for a PyfaceFont instance.

    Parameters
    ----------
    description : str
        A text description of the font in a CSS-style format.

    Returns
    -------
    properties : dict
        A dictionary of font properties suitable for passing to a Font as
        keyword arguments.
    """
    family = []
    weight = 'normal'
    stretch = 'normal'
    size = -1
    style = 'normal'
    variant_set = set()
    for token in token_re.finditer(description):
        kind = token.lastgroup
        value = token.group()
        index = token.start()
        if kind == 'SIZE':
            if size != -1:
                raise FontParseError(
                    f"Size declared twice in {description!r}"
                )
            value = value[:-2]
            try:
                size = float(value)
            except ValueError:
                raise FontParseError(
                    f"Invalid font size {value!r} at position {index} in {description!r}"
                )
        elif kind == 'NUMBER':
            if value in weights and weight == 'normal':
                weight = value
            elif size != -1:
                raise FontParseError(
                    f"Size declared twice in {description!r}"
                )
            else:
                try:
                    size = float(value)
                except ValueError:
                    raise FontParseError(
                        f"Invalid font size {value!r} at position {index} in {description!r}"
                    )
        elif kind == 'NAME':
            # substitute synonyms
            value = parser_synonyms.get(value, value)
            if value.lower() in weights:
                if weight != 'normal':
                    raise FontParseError(
                        f"Weight declared twice in {description!r}"
                    )
                weight = value.lower()
            elif value.lower() in stretches:
                if stretch != 'normal':
                    raise FontParseError(
                        f"Stretch declared twice in {description!r}"
                    )
                stretch = value.lower()
            elif value.lower() in sizes:
                if size != -1:
                    raise FontParseError(
                        f"Size declared twice in {description!r}"
                    )
                size = sizes[value.lower()]
            elif value.lower() in styles:
                if style != 'normal':
                    raise FontParseError(
                        f"Style declared twice in {description!r}"
                    )
                style = value.lower()
            elif value in variants:
                if value.lower() in variant_set:
                    raise FontParseError(
                        f"Variant {value!r} declared twice in {description!r}"
                    )
                variant_set.add(value.lower())
            else:
                # assume it is a font family name
                family.append(value)
        elif kind == 'QUOTED_NAME':
            family.append(value[1:-1])
        elif kind == 'MISMATCH':
            raise FontParseError(
                f"Parse error {value!r} at {index} in {description!r}"
            )
    if len(family) == 0:
        family = ['default']
    if size == -1:
        size = 12.0
    return {
        'family': family,
        'weight': weight,
        'stretch': stretch,
        'style': style,
        'variants': variant_set,
        'size': size,
    }


class Font(HasStrictTraits):
    """ A toolkit-independent font specification. """

    #: The preferred font families.
    family = FontFamily()

    #: The weight of the font.
    weight = FontWeight()

    #: How much the font is expanded or compressed.
    stretch = FontStretch()

    #: The style of the font.
    style = FontStyle()

    #: The size of the font.
    size = FontSize()

    #: The font variants.
    variants = FontVariants()

    @classmethod
    def from_description(cls, description):
        """ An extremely lax 'parser' for CSS-style font descriptions.

        Parameters
        ----------
        description : str
            A font description in string form such as
            'italic bold 14pt Helvetica, Arial, sans-serif' or
            '36pt "Comic Sans"'
        """
        return cls(**parse_font_description(description))

    @classmethod
    def from_toolkit(cls, toolkit_font):
        """ Create a Font from a toolkit font object.

        Parameters
        ----------
        toolkit_font : any
            A toolkit font to be converted to a corresponding class instance,
            within the limitations of the options supported by the class.
        """
        from pyface.toolkit import toolkit_object
        toolkit_font_to_properties = toolkit_object(
            'font:toolkit_font_to_properties')

        return cls(**toolkit_font_to_properties(toolkit_font))

    def to_toolkit(self):
        """ Create a toolkit font object from the Font instance.

        Returns
        -------
        toolkit_font : any
            A toolkit font which matches the property of the font as
            closely as possible given the constraints of the toolkit.
        """
        from pyface.toolkit import toolkit_object
        font_to_toolkit_font = toolkit_object('font:font_to_toolkit_font')

        return font_to_toolkit_font(self)

    def __str__(self):
        terms = []
        if self.style != 'normal':
            terms.append(self.style)
        terms.extend(
            variant for variant in variants
            if variant in self.variants
        )
        if self.weight != 'normal':
            terms.append(self.weight)
        if self.stretch != 'normal':
            terms.append(self.stretch)
        size = self.size
        # if size is an integer
        if int(size) == size:
            size = int(size)
        terms.append(f"{size}pt")
        terms.append(
            ', '.join(
                repr(family) if ' ' in family else family
                for family in self.family
            )
        )
        return ' '.join(terms)

    def __repr__(self):
        traits = self.trait_get(self.editable_traits())
        trait_args = ', '.join(
            f"{name}={value!r}"
            for name, value in traits.items()
        )
        return f"{self.__class__.__name__}({trait_args})"

    def __eq__(self, other):
        if isinstance(other, Font):
            return (
                self.family == other.family
                and self.weight == other.weight
                and self.stretch == other.stretch
                and self.style == other.style
                and self.size == other.size
                and self.variants == other.variants
            )
        else:
            return NotImplemented


class PyfaceFont(TraitType):
    """ A trait that holds a Pyface Font.

    The value can be assigned as a string, in which case it is parsed
    as a font description and an appropriate font created for it.
    """

    #: The default value should be a tuple (factory, args, kwargs)
    default_value_type = DefaultValue.callable_and_args

    def __init__(self, value=None, **metadata):
        if isinstance(value, Font):
            value = value.trait_get(value.editable_traits())
        if isinstance(value, str):
            value = parse_font_description(value)
        if isinstance(value, dict):
            # freeze the family list and variant set
            if 'family' in value:
                value['family'] = tuple(value['family'])
            if 'variants' in value:
                value['variants'] = frozenset(value['variants'])
            default_value = (Font, (), value.copy())
        elif value is None:
            default_value = (Font, (), {})
        else:
            raise TraitError(f"Invalid trait value {value!r}")
        super().__init__(default_value, **metadata)

    def validate(self, object, name, value):
        if isinstance(value, Font):
            return value
        elif isinstance(value, str):
            try:
                return Font.from_description(value)
            except FontParseError:
                self.error(object, name, value)
        else:
            self.error(object, name, value)

    def info(self):
        return (
            "a Pyface Font or a string describing a Pyface Font "
            "(eg. 'italic 12pt Arial, sans-serif' or "
            "'demibold 36pt \"Comic Sans\"')"
        )
