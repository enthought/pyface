# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
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
    These can be given as a percentage between 50% and 200%, or by strings
    such as as 'condensed' and 'expanded' that correspond to those values.

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
    BaseCFloat, CList, CSet, DefaultValue, Enum, HasStrictTraits, Map, Range,
    Str, TraitError, TraitType
)
from traits.trait_type import NoDefaultSpecified

WEIGHTS = {str(i): i for i in range(100, 1001, 100)}

# Note: we don't support 'medium' as an alias for weight 500 because it
# conflicts with the usage of 'medium' as an alias for a 12pt font in the CSS
# specification for font attributes.
WEIGHTS.update({
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

STRETCHES = {
    'ultra-condensed': 50,
    'ultracondensed': 62.5,
    'extra-condensed': 62.5,
    'extracondensed': 62.5,
    'condensed': 75,
    'semi-condensed': 87.5,
    'semicondensed': 87.5,
    'normal': 100,
    'semi-expanded': 112.5,
    'semiexpanded': 112.5,
    'expanded': 125,
    'extra-expanded': 150,
    'extraexpanded': 150,
    'ultra-expanded': 200,
    'ultraexpanded': 200,
}

SIZES = {
    'xx-small': 7.0,
    'x-small': 9.0,
    'small': 10.0,
    'medium': 12.0,
    'large': 14.0,
    'x-large': 18.0,
    'xx-large': 20.0,
}

STYLES = ('normal', 'italic', 'oblique')

VARIANTS = ['small-caps', 'underline', 'strikethrough', 'overline']

#: A trait for font families.
FontFamily = CList(Str, ['default'])

#: A trait for font weights.
FontWeight = Map(WEIGHTS, default_value='normal')

#: A trait for font styles.
FontStyle = Enum(STYLES)

#: A trait for font variant properties.
FontVariants = CSet(Enum(VARIANTS))


class FontStretch(BaseCFloat):
    """ Trait type for font stretches.

    The is a CFloat trait which also allows values which are keys of the
    stretch dictionary.  Values must be floats between 50 and 200, inclusive.
    """

    #: The default value for the trait.
    default_value = 100.0

    def __init__(self, default_value=NoDefaultSpecified, **metadata):
        if default_value != NoDefaultSpecified:
            default_value = self.validate(None, None, default_value)
        super().__init__(default_value, **metadata)

    def validate(self, object, name, value):
        if isinstance(value, str) and value.endswith('%'):
            value = value[:-1]
        value = STRETCHES.get(value, value)
        value = super().validate(object, name, value)
        if not 50 <= value <= 200:
            self.error(object, name, value)
        return value

    def info(self):
        info = (
            "a float from 50 to 200, "
            "a value that can convert to a float from 50 to 200, "
        )
        info += ', '.join(repr(key) for key in SIZES)
        info += (
            " or a string with a float value from 50 to 200 followed by '%'"
        )
        return info


class FontSize(BaseCFloat):
    """ Trait type for font sizes.

    The is a CFloat trait which also allows values which are keys of the
    size dictionary, and also ignores trailing 'pt' ot 'px' annotation in
    string values.  The value stored is a float.
    """

    #: The default value for the trait.
    default_value = 12.0

    def __init__(self, default_value=NoDefaultSpecified, **metadata):
        if default_value != NoDefaultSpecified:
            default_value = self.validate(None, None, default_value)
        super().__init__(default_value, **metadata)

    def validate(self, object, name, value):
        if isinstance(value, str) and (
                    value.endswith('pt') or value.endswith('px')):
            value = value[:-2]
        value = SIZES.get(value, value)
        value = super().validate(object, name, value)
        if value <= 0:
            self.error(object, name, value)
        return value

    def info(self):
        info = (
            "a positive float, a value that can convert to a positive float, "
        )
        info += ', '.join(repr(key) for key in SIZES)
        info += (
            " or a string with a positive float value followed by 'pt' or 'px'"
        )
        return info


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
        """ Produce a CSS-style representation of the font. """
        terms = []
        if self.style != 'normal':
            terms.append(self.style)
        terms.extend(
            variant for variant in VARIANTS
            if variant in self.variants
        )
        if self.weight != 'normal':
            terms.append(self.weight)
        if self.stretch != 100:
            terms.append("{:g}%".format(self.stretch))
        size = self.size
        # if size is an integer
        if int(size) == size:
            size = int(size)
        terms.append("{}pt".format(size))
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
            "{}={!r}".format(name, value)
            for name, value in traits.items()
        )
        return "{}({})".format(self.__class__.__name__, trait_args)

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
