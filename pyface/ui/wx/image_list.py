# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A cached image list. """


import wx


from .image_resource import ImageResource


# fixme: rename to 'CachedImageList'?!?
class ImageList(wx.ImageList):
    """ A cached image list. """

    def __init__(self, width, height):
        """ Creates a new cached image list. """

        # Base-class constructor.
        wx.ImageList.__init__(self, width, height)

        self._width = width
        self._height = height

        # Cache of the indexes of the images in the list!
        self._cache = {}  # {filename : index}

        return

    # ------------------------------------------------------------------------
    # 'ImageList' interface.
    # ------------------------------------------------------------------------

    def GetIndex(self, filename):
        """ Returns the index of the specified image.

        The image will be loaded and added to the image list if it is not
        already there.

        """

        # Try the cache first.
        index = self._cache.get(filename)
        if index is None:
            # Were we passed an image resource?
            if isinstance(filename, ImageResource):
                # Create an image.
                image = filename.create_image(size=(self._width, self._height))

            # If the filename is a string then it is the filename of some kind
            # of image (e.g 'foo.gif', 'image/foo.png' etc).
            elif isinstance(filename, str):
                # Load the image from the file.
                image = wx.Image(filename, wx.BITMAP_TYPE_ANY)

            # Otherwise the filename is *actually* an icon (in our case,
            # probably related to a MIME type).
            else:
                # Create a bitmap from the icon.
                bmp = wx.Bitmap(self._width, self._height)
                bmp.CopyFromIcon(filename)

                # Turn it into an image so that we can scale it.
                image = wx.ImageFromBitmap(bmp)

            # We force all images in the cache to be the same size.
            self._scale(image)

            # We also force them to be bitmaps!
            bmp = image.ConvertToBitmap()

            # Add the bitmap to the actual list...
            index = self.Add(bmp)

            # ... and update the cache.
            self._cache[filename] = index

        return index

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _scale(self, image):
        """ Scales the specified image (if necessary). """

        if (
            image.GetWidth() != self._width
            or image.GetHeight() != self._height
        ):
            image.Rescale(self._width, self._height)

        return image
