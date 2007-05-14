#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------

# Major package imports.
import wx


class ImageCache_wx(object):
    """ The ImageCache monkey patch for wx. """

    ###########################################################################
    # 'ImageCache toolkit interface.
    ###########################################################################

    def _tk_imagecache_init_cache(self):
        """ Initialise the cache. """

        # The images in the cache!
        self._images = {} # {filename : wx.Image}

        # The images in the cache converted to bitmaps.
        self._bitmaps = {} # {filename : wx.Bitmap}
        
        return

    def _tk_imagecache_get_image(self, filename):
        """ Returns the specified image. """

        # Try the cache first.
        image = self._images.get(filename)
        if image is None:
            # Load the image from the file and add it to the list.
            #
            # N.B 'wx.BITMAP_TYPE_ANY' tells wxPython to attempt to autodetect
            # --- the image format.
            image = wx.Image(filename, wx.BITMAP_TYPE_ANY)

            # We force all images in the cache to be the same size.
            if image.GetWidth() != self._width or image.GetHeight() != self._height:
                image.Rescale(self._width, self._height)

            # Add the bitmap to the cache!
            self._images[filename] = image

        return image

    def _tk_imagecache_get_bitmap(self, filename):
        """ Returns the specified image as a bitmap. """

        # Try the cache first.
        bmp = self._bitmaps.get(filename)
        if bmp is None:
            # Get the image.
            image = self.get_image(filename)

            # Convert the alpha channel to a mask.
            image.ConvertAlphaToMask()

            # Convert it to a bitmaps!
            bmp = image.ConvertToBitmap()

            # Add the bitmap to the cache!
            self._bitmaps[filename] = bmp

        return bmp
            
#### EOF ######################################################################
