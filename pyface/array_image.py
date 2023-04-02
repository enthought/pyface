# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Array, HasStrictTraits, provides

from pyface.i_image import IImage
from pyface.util.image_helpers import (
    array_to_image, image_to_bitmap, bitmap_to_icon, resize_image
)

#: Trait type for image arrays.
ImageArray = Array(shape=(None, None, (3, 4)), dtype='uint8')


@provides(IImage)
class ArrayImage(HasStrictTraits):
    """ An IImage stored in an RGB(A) numpy array.
    """

    # 'ArrayImage' interface ------------------------------------------------

    #: The bytes of the image.
    data = ImageArray()

    # ------------------------------------------------------------------------
    # 'IImage' interface.
    # ------------------------------------------------------------------------

    def create_image(self, size=None):
        """ Creates a toolkit-specific image for this array.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        image : toolkit image
            The toolkit image corresponding to the image and the specified
            size.
        """
        image = array_to_image(self.data)
        if size is not None:
            image = resize_image(image, size)
        return image

    def create_bitmap(self, size=None):
        """ Creates a toolkit-specific bitmap image for this array.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        image : toolkit bitmap
            The toolkit bitmap corresponding to the image and the specified
            size.
        """
        return image_to_bitmap(self.create_image(size))

    def create_icon(self, size=None):
        """ Creates a toolkit-specific icon for this array.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default icon size.

        Returns
        -------
        image : toolkit icon
            The toolkit image corresponding to the image and the specified
            size as an icon.
        """
        return bitmap_to_icon(self.create_bitmap(size))

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, data, **traits):
        super().__init__(data=data, **traits)
