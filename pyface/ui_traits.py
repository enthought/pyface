# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Defines common traits used within the pyface library. """
from collections.abc import Sequence
import logging

try:
    import numpy as np
except ImportError:
    np = None

from traits.api import (
    ABCHasStrictTraits,
    DefaultValue,
    Enum,
    Range,
    TraitError,
    TraitFactory,
    TraitType,
)
from traits.trait_base import get_resource_path

from pyface.color import Color
from pyface.font import Font
from pyface.i_image import IImage
from pyface.util.color_parser import ColorParseError
from pyface.util.font_parser import simple_parser, FontParseError


logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------
#  Images
# -------------------------------------------------------------------------------

# cache of lookups from string to ImageResource instance
image_resource_cache = {}

# cache of conversions of ImageResource instances to toolkit bitmaps
image_bitmap_cache = {}


def convert_image(value, level=3):
    """ Converts a specified value to an ImageResource if possible.
    """
    if not isinstance(value, str):
        return value

    key = value
    is_pyface_image = value.startswith("@")
    if not is_pyface_image:
        search_path = get_resource_path(level)
        key = "%s[%s]" % (value, search_path)

    result = image_resource_cache.get(key)
    if result is None:
        if is_pyface_image:
            try:
                from .image.image import ImageLibrary

                result = ImageLibrary.image_resource(value)
            except Exception as exc:
                logger.error("Can't load image resource '%s'." % value)
                logger.exception(exc)
                result = None
        else:
            from pyface.image_resource import ImageResource

            result = ImageResource(value, search_path=[search_path])

        image_resource_cache[key] = result

    return result


def convert_bitmap(image):
    """ Converts an ImageResource to a bitmap using a cache.
    """
    from pyface.i_image_resource import IImageResource
    if not isinstance(image, IImageResource):
        # don't try to cache non-ImageResource IImages as they may be
        # dynamically changing
        return image.create_bitmap()

    bitmap = image_bitmap_cache.get(image)
    if (bitmap is None) and (image is not None):
        image_bitmap_cache[image] = bitmap = image.create_bitmap()

    return bitmap


class Image(TraitType):
    """ Defines a trait whose value must be a IImage or a string
        that can be converted to an IImageResource.
    """

    #: Define the default value for the trait.
    default_value = None

    #: A description of the type of value this trait accepts.
    info_text = "an IImage or string that can be used to define an ImageResource"  # noqa: E501

    def __init__(self, value=None, **metadata):
        """ Creates an Image trait.

        Parameters
        ----------
        value : string or ImageResource
            The default value for the Image, either an IImage object,
            or a string from which an ImageResource object can be derived.
        """
        super().__init__(convert_image(value), **metadata)

    def validate(self, object, name, value):
        """ Validates that a specified value is valid for this trait.
        """
        if value is None:
            return None

        new_value = convert_image(value, 4)
        if isinstance(new_value, IImage):
            return new_value

        self.error(object, name, value)

    def create_editor(self):
        """ Returns the default UI editor for the trait.
        """
        from traitsui.editors.api import ImageEditor

        return ImageEditor()


# -------------------------------------------------------------------------------
#  Color
# -------------------------------------------------------------------------------


class PyfaceColor(TraitType):
    """ A Trait which casts strings and tuples to a Pyface Color value.
    """

    #: The default value should be a tuple (factory, args, kwargs).
    default_value_type = DefaultValue.callable_and_args

    def __init__(self, value=None, **metadata):
        if value is not None:
            color = self.validate(None, None, value)
            default_value = (Color, (), {'rgba': color.rgba})
        else:
            default_value = (Color, (), {})
        super().__init__(default_value, **metadata)

    def validate(self, object, name, value):
        """Validate the trait

        This accepts, Color values, parseable strings and RGB(A) sequences
        (including numpy arrays).
        """
        if isinstance(value, Color):
            return value
        if isinstance(value, str):
            try:
                return Color.from_str(value)
            except ColorParseError:
                self.error(object, name, value)
        is_array = (
            np is not None
            and isinstance(value, (np.ndarray, np.void))
        )
        if is_array or isinstance(value, Sequence):
            channels = tuple(value)
            if len(channels) == 4:
                return Color(rgba=channels)
            elif len(channels) == 3:
                return Color(rgb=channels)

        self.error(object, name, value)

    def info(self):
        """Describe the trait"""
        return (
            "a Pyface Color, a #-hexadecimal rgb or rgba string,  a standard "
            "color name, or a sequence of RGBA or RGB values between 0 and 1"
        )


# -------------------------------------------------------------------------------
#  Font
# -------------------------------------------------------------------------------


class PyfaceFont(TraitType):
    """ A Trait which casts strings to a Pyface Font value.
    """

    #: The default value should be a tuple (factory, args, kwargs)
    default_value_type = DefaultValue.callable_and_args

    #: The parser to use when converting text to keyword args.  This should
    #: accept a string and return a dictionary of Font class trait values (ie.
    #: "family", "size", "weight", etc.).
    parser = None

    def __init__(self, value=None, *, parser=simple_parser, **metadata):
        self.parser = parser
        if value is not None:
            try:
                font = self.validate(None, None, value)
            except TraitError:
                raise ValueError(
                    "expected " + self.info()
                    + f", but got {value!r}"
                )
            default_value = (
                Font,
                (),
                font.trait_get(transient=lambda x: not x),
            )
        else:
            default_value = (Font, (), {})
        super().__init__(default_value, **metadata)

    def validate(self, object, name, value):
        """Validate the trait

        This accepts, Font values and parseable strings.
        """
        if isinstance(value, Font):
            return value
        if isinstance(value, str):
            try:
                return Font(**self.parser(value))
            except FontParseError:
                self.error(object, name, value)

        self.error(object, name, value)

    def info(self):
        """Describe the trait"""
        return (
            "a Pyface Font, or a string describing a Pyface Font"
        )


# -------------------------------------------------------------------------------
#  Borders, Margins and Layout
# -------------------------------------------------------------------------------


class BaseMB(ABCHasStrictTraits):
    """ Base class for Margins and Borders

    The constructor of this class maps posiitonal arguments to traits.

    - If one value is provided it is taken as the value for all sides.
    - If two values are provided, then the first argument is used for
      left and right, while the second is used for top and bottom.
    - If 4 values are provided, then the arguments are mapped to
      left, right, top, and bottom, respectively.
    """

    def __init__(self, *args, **traits):
        n = len(args)
        if n > 0:
            if n == 1:
                left = right = top = bottom = args[0]
            elif n == 2:
                left = right = args[0]
                top = bottom = args[1]
            elif n == 4:
                left, right, top, bottom = args
            else:
                raise TraitError(
                    "0, 1, 2 or 4 arguments expected, but %d " "specified" % n
                )
            traits.update(
                {"left": left, "right": right, "top": top, "bottom": bottom}
            )

        super().__init__(**traits)


class Margin(BaseMB):
    """A HasTraits class that holds margin sizes."""

    #: The amount of padding/margin at the top.
    top = Range(-32, 32, 0)

    #: The amount of padding/margin at the bottom.
    bottom = Range(-32, 32, 0)

    #: The amount of padding/margin on the left.
    left = Range(-32, 32, 0)

    #: The amount of padding/margin on the right.
    right = Range(-32, 32, 0)


class Border(BaseMB):
    """A HasTraits class that holds border thicknesses."""

    #: The amount of border at the top.
    top = Range(0, 32, 0)

    #: The amount of border at the bottom.
    bottom = Range(0, 32, 0)

    #: The amount of border on the left.
    left = Range(0, 32, 0)

    #: The amount of border on the right.
    right = Range(0, 32, 0)


class HasMargin(TraitType):
    """ Defines a trait whose value must be a Margin object or an integer or
        tuple value that can be converted to one.
    """

    #: The desired value class.
    klass = Margin

    #: Define the default value for the trait.
    default_value = Margin(0)

    #: A description of the type of value this trait accepts.
    info_text = (
        "a Margin instance, or an integer in the range from -32 to 32 "
        "or a tuple with 1, 2 or 4 integers in that range that can be "
        "used to define one"
    )

    def validate(self, object, name, value):
        """ Validates that a specified value is valid for this trait.
        """
        if isinstance(value, int):
            try:
                value = self.klass(value)
            except Exception:
                self.error(object, name, value)
        elif isinstance(value, tuple):
            try:
                value = self.klass(*value)
            except Exception:
                self.error(object, name, value)

        if isinstance(value, self.klass):
            return value

        self.error(object, name, value)

    def get_default_value(self):
        """ Returns a tuple of the form:
                (default_value_type, default_value)

            which describes the default value for this trait.
        """
        dv = self.default_value
        dvt = self.default_value_type
        if dvt < 0:
            if isinstance(dv, int):
                dv = self.klass(dv)
            elif isinstance(dv, tuple):
                dv = self.klass(*dv)

            if not isinstance(dv, self.klass):
                return super().get_default_value()

            self.default_value_type = dvt = DefaultValue.callable_and_args
            dv = (self.klass, (), dv.trait_get())

        return (dvt, dv)


class HasBorder(HasMargin):
    """ Defines a trait whose value must be a Border object or an integer
        or tuple value that can be converted to one.
    """

    #: The desired value class.
    klass = Border

    #: Define the default value for the trait.
    default_value = Border(0)

    #: A description of the type of value this trait accepts.
    info_text = (
        "a Border instance, or an integer in the range from 0 to 32 "
        "or a tuple with 1, 2 or 4 integers in that range that can be "
        "used to define one"
    )


#: The position of an image relative to its associated text.
Position = Enum("left", "right", "above", "below")

#: The alignment of text within a control.
Alignment = Enum("default", "left", "center", "right")

#: Whether the orientation of a widget's contents is horizontal or vertical.
Orientation = Enum("vertical", "horizontal")


# -------------------------------------------------------------------------------
#  Legacy TraitsUI Color and Font Traits
# -------------------------------------------------------------------------------

def TraitsUIColor(*args, **metadata):
    """ Returns a trait whose value must be a GUI toolkit-specific color.

    This is copied from the deprecated trait that is in traits.api.  It adds
    a deferred dependency on TraitsUI.

    This trait will be replaced by native Pyface color traits in Pyface 8.0.
    New code should not use this trait.
    """
    from traitsui.toolkit_traits import ColorTrait

    return ColorTrait(*args, **metadata)


TraitsUIColor = TraitFactory(TraitsUIColor)


def TraitsUIFont(*args, **metadata):
    """ Returns a trait whose value must be a GUI toolkit-specific font.

    This is copied from the deprecated trait that is in traits.api.  It adds
    a deferred dependency on TraitsUI.

    This trait will be replaced by native Pyface font traits in Pyface 8.0.
    New code should not use this trait.
    """
    from traitsui.toolkit_traits import FontTrait

    return FontTrait(*args, **metadata)


TraitsUIFont = TraitFactory(TraitsUIFont)
