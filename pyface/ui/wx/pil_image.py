# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx

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
        """ Creates a Wx image for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.  This is currently ignored.

        Returns
        -------
        image : wx.Image
            The toolkit image corresponding to the image and the specified
            size.
        """
        # XXX ignore size requests - rescaling might require better caching
        image = self.image
        wx_image = wx.EmptyImage(self.image.size[0], self.image.size[1])
        wx_image.SetData(image.convert("RGB").tobytes())
        if image.mode == "RGBA":
            wx_image.InitAlpha()
            wx_image.SetAlpha(image.getchannel("A").tobytes())
        return wx_image

    def create_bitmap(self, size=None):
        """ Creates a Wx bitmap image for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.  This is currently ignored.

        Returns
        -------
        image : wx.Bitmap
            The toolkit bitmap corresponding to the image and the specified
            size.
        """
        return self.create_image(size).ConvertToBitmap()

    def create_icon(self, size=None):
        """ Creates a Wx icon for this image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default icon size.  This is currently ignored.

        Returns
        -------
        image : wx.Icon
            The toolkit image corresponding to the image and the specified
            size as an icon.
        """
        icon = wx.Icon()
        icon.CopyFromBitmap(self.create_bitmap(size))
        return icon
