# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import provides

from pyface.i_pil_image import IPILImage, MPILImage
from pyface.ui.qt4.util.image_helpers import resize_image


@provides(IPILImage)
class PILImage(MPILImage):
    """ The toolkit specific implementation of a PILImage.
    """

    #: An internal cache of images by size.
    _image_cache = Dict()

    # ------------------------------------------------------------------------
    # 'IImage' interface.
    # ------------------------------------------------------------------------

    def create_image(self, size=None):
        """ Creates a Qt image for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a (width, height) tuple, or None if wanting
            default image size.

        Returns
        -------
        image : QImage
            The toolkit image corresponding to the image and the specified
            size.
        """
        # use the cache of images to ensure referential integrity of images
        # when being used
        if size not in self._image_cache:
            from PIL.ImageQt import ImageQt
            image = ImageQt(self.image)
            if size is not None:
                image = resize_image(image, size)
            self._image_cache[size] = image
        return self._image_cache[size]
