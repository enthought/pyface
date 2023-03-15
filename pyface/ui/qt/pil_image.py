# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
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
from pyface.ui.qt.util.image_helpers import resize_image


@provides(IPILImage)
class PILImage(MPILImage):
    """ The toolkit specific implementation of a PILImage.
    """

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
        from PIL.ImageQt import ImageQt
        image = ImageQt(self.image)
        if size is not None:
            return resize_image(image, size)
        else:
            return image
