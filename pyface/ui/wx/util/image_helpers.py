# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Helper functions for working with images

This module provides helper functions for converting between numpy arrays
and Qt wx.Images, as well as between the various image types in a standardized
way.
"""

from enum import IntEnum

import wx


class ScaleMode(IntEnum):
    fast = wx.IMAGE_QUALITY_NORMAL
    smooth = wx.IMAGE_QUALITY_HIGH


class AspectRatio(IntEnum):
    ignore = 0
    keep_constrain = 1
    keep_expand = 2


def image_to_bitmap(image):
    """ Convert a wx.Image to a wx.Bitmap.

    Parameters
    ----------
    image : wx.Image
        The wx.Image to convert.

    Return
    ------
    bitmap : wx.Bitmap
        The corresponding wx.Bitmap.
    """
    return image.ConvertToBitmap()


def bitmap_to_image(bitmap):
    """ Convert a wx.Bitmap to a wx.Image.

    Parameters
    ----------
    bitmap : wx.Bitmap
        The wx.Bitmap to convert.

    Return
    ------
    image : wx.Image
        The corresponding wx.Image.
    """
    return bitmap.ConvertToImage()


def bitmap_to_icon(bitmap):
    """ Convert a wx.Bitmap to a wx.Icon.

    Parameters
    ----------
    bitmap : wx.Bitmap
        The wx.Bitmap to convert.

    Return
    ------
    icon : wx.Icon
        The corresponding wx.Icon.
    """
    return wx.Icon(bitmap)


def resize_image(image, size, aspect_ratio=AspectRatio.ignore,
                 mode=ScaleMode.fast):
    """ Resize a toolkit image to the given size. """
    image_size = image.GetSize()
    width, height = _get_size_for_aspect_ratio(image_size, size, aspect_ratio)
    return image.Scale(width, height, mode)


def resize_bitmap(bitmap, size, aspect_ratio=AspectRatio.ignore,
                  mode=ScaleMode.fast):
    """ Resize a toolkit bitmap to the given size. """
    image = bitmap_to_image(bitmap)
    image = resize_image(image, size, aspect_ratio, mode)
    return image_to_bitmap(image)


def image_to_array(image):
    """ Convert a wx.Image to a numpy array.

    This copies the data returned from wx.

    Parameters
    ----------
    image : wx.Image
        The wx.Image that we want to extract the values from.  The format must
        be either RGB32 or ARGB32.

    Return
    ------
    array : ndarray
        An N x M x 4 array of unsigned 8-bit ints as RGBA values.
    """
    import numpy as np

    width, height = image.GetSize()
    rgb_data = np.array(image.GetData(), dtype='uint8').reshape(width, height, 3)
    if image.HasAlpha():
        alpha = np.array(image.GetAlpha(), dtype='uint8').reshape(width, height)
    else:
        alpha = np.full((width, height), 0xff, dtype='uint8')
    array = np.empty(shape=(width, height, 4), dtype='uint8')
    array[:, :, :3] = rgb_data
    array[:, :, 3] = alpha
    return array


def array_to_image(array):
    """ Convert a numpy array to a wx.Image.

    This copies the data before passing it to wx.

    Parameters
    ----------
    array : ndarray
        An N x M x {3, 4} array of unsigned 8-bit ints.  The image
        format is assumed to be RGB or RGBA, based on the shape.

    Return
    ------
    image : wx.Image
        The wx.Image created from the data.
    """
    if array.ndim != 3:
        raise ValueError("Array must be either RGB or RGBA values.")

    height, width, channels = array.shape

    if channels == 3:
        image = wx.Image(width, height, array.tobytes())
    elif channels == 4:
        image = wx.Image(
            width,
            height,
            array[..., :3].tobytes(),
            array[..., 3].tobytes(),
        )
    else:
        raise ValueError("Array must be either RGB or RGBA values.")

    return image


def _get_size_for_aspect_ratio(image_size, size, aspect_ratio):
    width, height = size
    image_width, image_height = image_size
    if aspect_ratio != AspectRatio.ignore:
        if aspect_ratio == AspectRatio.keep_constrain:
            scale = min(width/image_width, height/image_height)
        else:
            scale = max(width/image_width, height/image_height)
        width = int(round(scale * image_width))
        height = int(round(scale * image_height))
    return (width, height)
