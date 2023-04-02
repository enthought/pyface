# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The interface for a PIL Image. """

from traits.api import HasStrictTraits, Instance

from pyface.i_image import IImage


class IPILImage(IImage):
    """ The interface for a image that wraps a PIL Image.
    """

    # 'IPILImage' interface --------------------------------------------

    #: The PIL Image instance.
    image = Instance("PIL.Image.Image")


class MPILImage(HasStrictTraits):
    """ The base implementation mixin for a image that wraps a PIL Image.
    """

    # 'IPILImage' interface --------------------------------------------

    #: The PIL Image instance.
    image = Instance("PIL.Image.Image")

    def __init__(self, image, **traits):
        super().__init__(image=image, **traits)

    def create_bitmap(self, size=None):
        """ Creates a bitmap image for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a (width, height) tuple, or None if wanting
            default image size.

        Returns
        -------
        image : bitmap
            The toolkit bitmap corresponding to the image and the specified
            size.
        """
        from pyface.util.image_helpers import image_to_bitmap
        return image_to_bitmap(self.create_image(size))

    def create_icon(self, size=None):
        """ Creates an icon for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a (width, height) tuple, or None if wanting
            default icon size.

        Returns
        -------
        image : icon
            The toolkit image corresponding to the image and the specified
            size as an icon.
        """
        from pyface.util.image_helpers import bitmap_to_icon
        return bitmap_to_icon(self.create_bitmap(size))
