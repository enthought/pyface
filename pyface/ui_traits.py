#------------------------------------------------------------------------------
#
#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: Enthought Developers
#
#------------------------------------------------------------------------------

""" Defines common traits used within the pyface library. """
import logging

from traits.api import ABCHasStrictTraits, Enum, Range, TraitError, TraitType
from traits.trait_base import get_resource_path
try:
    from traits.trait_handlers import CALLABLE_AND_ARGS_DEFAULT_VALUE
except ImportError:
    CALLABLE_AND_ARGS_DEFAULT_VALUE = 7
import six


logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
#  Images
#-------------------------------------------------------------------------------

image_resource_cache = {}
image_bitmap_cache = {}


def convert_image(value, level=3):
    """ Converts a specified value to an ImageResource if possible.
    """
    if not isinstance( value, six.string_types ):
        return value

    key = value
    is_pyface_image = value.startswith('@')
    if not is_pyface_image:
        search_path = get_resource_path(level)
        key = '%s[%s]' % (value, search_path)

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


def convert_bitmap(image_resource):
    """ Converts an ImageResource to a bitmap using a cache.
    """
    bitmap = image_bitmap_cache.get(image_resource)
    if (bitmap is None) and (image_resource is not None):
        image_bitmap_cache[image_resource] = bitmap = \
            image_resource.create_bitmap()

    return bitmap


class Image(TraitType):
    """ Defines a trait whose value must be a ImageResource or a string
        that can be converted to one.
    """

    # Define the default value for the trait:
    default_value = None

    # A description of the type of value this trait accepts:
    info_text = 'an ImageResource or string that can be used to define one'

    def __init__(self, value=None, **metadata):
        """ Creates an Image trait.

        Parameters
        ----------
        value : string or ImageResource
            The default value for the Image, either an ImageResource object,
            or a string from which an ImageResource object can be derived.
        """
        super(Image, self).__init__(convert_image(value), **metadata)

    def validate(self, object, name, value):
        """ Validates that a specified value is valid for this trait.
        """
        from pyface.i_image_resource import IImageResource

        if value is None:
            return None

        new_value = convert_image(value, 4)
        if isinstance(new_value, IImageResource):
            return new_value

        self.error(object, name, value)

    def create_editor(self):
        """ Returns the default UI editor for the trait.
        """
        from traitsui.editors.api import ImageEditor
        return ImageEditor()


#-------------------------------------------------------------------------------
#  Borders, Margins and Layout
#-------------------------------------------------------------------------------

class BaseMB(ABCHasStrictTraits):

    def __init__(self, *args, **traits):
        """ Map posiitonal arguments to traits.

        If one value is provided it is taken as the value for all sides.
        If two values are provided, then the first argument is used for
        left and right, while the second is used for top and bottom.
        If 4 values are provided, then the arguments are mapped to
        left, right, top, and bottom, respectively.
        """
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
                raise TraitError('0, 1, 2 or 4 arguments expected, but %d '
                                 'specified' % n)
            traits.update({'left': left, 'right': right,
                           'top': top, 'bottom': bottom})

        super(BaseMB, self).__init__(**traits)


class Margin(BaseMB):

    # The amount of padding/margin at the top:
    top = Range(-32, 32, 0)

    # The amount of padding/margin at the bottom:
    bottom = Range(-32, 32, 0)

    # The amount of padding/margin on the left:
    left = Range(-32, 32, 0)

    # The amount of padding/margin on the right:
    right = Range(-32, 32, 0)


class Border(BaseMB):

    # The amount of border at the top:
    top = Range(0, 32, 0)

    # The amount of border at the bottom:
    bottom = Range(0, 32, 0)

    # The amount of border on the left:
    left = Range(0, 32, 0)

    # The amount of border on the right:
    right = Range(0, 32, 0)


class HasMargin(TraitType):
    """ Defines a trait whose value must be a Margin object or an integer or
        tuple value that can be converted to one.
    """

    # The desired value class:
    klass = Margin

    # Define the default value for the trait:
    default_value = Margin(0)

    # A description of the type of value this trait accepts:
    info_text = ('a Margin instance, or an integer in the range from -32 to 32 '
                 'or a tuple with 1, 2 or 4 integers in that range that can be '
                 'used to define one')

    def validate (self, object, name, value):
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
        dv  = self.default_value
        dvt = self.default_value_type
        if dvt < 0:
            if isinstance(dv, int):
                dv = self.klass(dv)
            elif isinstance(dv, tuple):
                dv = self.klass(*dv)

            if not isinstance(dv, self.klass):
                return super(HasMargin, self).get_default_value()

            self.default_value_type = dvt = CALLABLE_AND_ARGS_DEFAULT_VALUE
            dv = (self.klass, (), dv.trait_get())

        return (dvt, dv)


class HasBorder(HasMargin):
    """ Defines a trait whose value must be a Border object or an integer
        or tuple value that can be converted to one.
    """

    # The desired value class:
    klass = Border

    # Define the default value for the trait:
    default_value = Border(0)

    # A description of the type of value this trait accepts:
    info_text = ('a Border instance, or an integer in the range from 0 to 32 '
                 'or a tuple with 1, 2 or 4 integers in that range that can be '
                 'used to define one')


#: The position of an image relative to its associated text.
Position = Enum('left', 'right', 'above', 'below')

#: The alignment of text within a control.
Alignment = Enum('default', 'left', 'center', 'right')
