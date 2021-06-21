# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.qt.QtGui import QIcon, QPixmap

from traits.api import provides

from pyface.i_pil_image import IPILImage, MPILImage


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
            The desired size as a width, height tuple, or None if wanting
            default image size.  This is currently ignored.

        Returns
        -------
        image : QImage
            The toolkit image corresponding to the image and the specified
            size.
        """
        # XXX ignore size requests - rescaling might require better caching
        from PIL.ImageQt import ImageQt
        return ImageQt(self.image)

    def create_bitmap(self, size=None):
        """ Creates a Qt bitmap image for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.  This is currently ignored.

        Returns
        -------
        image : QPixmap
            The toolkit bitmap corresponding to the image and the specified
            size.
        """
        return QPixmap.fromImage(self.create_image(size))

    def create_icon(self, size=None):
        """ Creates a Qt icon for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default icon size.  This is currently ignored.

        Returns
        -------
        image : QIcon
            The toolkit image corresponding to the image and the specified
            size as an icon.
        """
        return QIcon(self.create_bitmap(size))
