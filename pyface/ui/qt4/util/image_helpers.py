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
and Qt QImages, as well as between the various image types in a standardized
way.
"""

from enum import Enum

from pyface.qt import qt_api
from pyface.qt.QtCore import Qt
from pyface.qt.QtGui import QImage, QPixmap, QIcon


class ScaleMode(Enum):
    fast = Qt.TransformationMode.FastTransformation
    smooth = Qt.TransformationMode.SmoothTransformation


class AspectRatio(Enum):
    ignore = Qt.AspectRatioMode.IgnoreAspectRatio
    keep_constrain = Qt.AspectRatioMode.KeepAspectRatio
    keep_expand = Qt.AspectRatioMode.KeepAspectRatioByExpanding


def image_to_bitmap(image):
    """ Convert a QImage to a QPixmap.
    Parameters
    ----------
    image : QImage
        The QImage to convert.

    Return
    ------
    bitmap : QPixmap
        The corresponding QPixmap.
    """
    bitmap = QPixmap.fromImage(image)
    # keep a reference to the QImage to ensure underlying data is available
    bitmap._image = image
    return bitmap


def bitmap_to_image(bitmap):
    """ Convert a QPixmap to a QImage.
    Parameters
    ----------
    bitmap : QPixmap
        The QPixmap to convert.

    Return
    ------
    image : QImage
        The corresponding QImage.
    """
    return bitmap.toImage()


def bitmap_to_icon(bitmap):
    """ Convert a QPixmap to a QIcon.
    Parameters
    ----------
    bitmap : QPixmap
        The QPixmap to convert.

    Return
    ------
    icon : QIcon
        The corresponding QIcon.
    """
    return QIcon(bitmap)


def resize_image(image, size, aspect_ratio=AspectRatio.ignore,
                 mode=ScaleMode.fast):
    """ Resize a toolkit image to the given size. """
    return image.scaled(*size, aspect_ratio.value, mode.value)


def resize_bitmap(bitmap, size, aspect_ratio=AspectRatio.ignore,
                  mode=ScaleMode.fast):
    """ Resize a toolkit bitmap to the given size. """
    return bitmap.scaled(*size, aspect_ratio.value, mode.value)


def image_to_array(image):
    """ Convert a QImage to a numpy array.

    This copies the data returned from Qt.

    Parameters
    ----------
    image : QImage
        The QImage that we want to extract the values from.  The format must
        be either RGB32 or ARGB32.

    Return
    ------
    array : ndarray
        An N x M x 4 array of unsigned 8-bit ints as RGBA values.
    """
    import numpy as np

    width, height = image.width(), image.height()
    channels = image.pixelFormat().channelCount()
    data = image.bits()
    if qt_api in {'pyqt', 'pyqt5'}:
        data = data.asarray(width * height * channels)
    array = np.array(data, dtype='uint8')
    array.shape = (height, width, channels)
    if image.format() in {QImage.Format.Format_RGB32, QImage.Format.Format_ARGB32}:
        # comes in as BGRA, but want RGBA
        array = array[:, :, [2, 1, 0, 3]]
    else:
        raise ValueError(
            "Unsupported QImage format {}".format(image.format())
        )
    return array


def array_to_image(array):
    """ Convert a numpy array to a QImage.

    This copies the data before passing it to Qt.

    Parameters
    ----------
    array : ndarray
        An N x M x {3, 4} array of unsigned 8-bit ints.  The image
        format is assumed to be RGB or RGBA, based on the shape.

    Return
    ------
    image : QImage
        The QImage created from the data.  The pixel format is
        QImage.Format.Format_RGB32.
    """
    import numpy as np

    if array.ndim != 3:
        raise ValueError("Array must be either RGB or RGBA values.")

    height, width, channels = array.shape
    data = np.empty((height, width, 4), dtype='uint8')
    if channels == 3:
        data[:, :, [2, 1, 0]] = array
        data[:, :, 3] = 0xff
    elif channels == 4:
        data[:, :, [2, 1, 0, 3]] = array
    else:
        raise ValueError("Array must be either RGB or RGBA values.")

    bytes_per_line = 4 * width

    if channels == 3:
        image = QImage(data.data, width, height, bytes_per_line,
                       QImage.Format.Format_RGB32)

    elif channels == 4:
        image = QImage(data.data, width, height, bytes_per_line,
                       QImage.Format.Format_ARGB32)
    # keep a reference to the array to ensure underlying data is available
    image._numpy_data = data
    return image
