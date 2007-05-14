#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class ImageCache_qt4(object):
    """ The ImageCache monkey patch for Qt4. """

    ###########################################################################
    # 'ImageCache toolkit interface.
    ###########################################################################

    def _tk_imagecache_get_image(self, filename):
        """ Returns the specified image. """

        image = QtGui.QPixmap(self._width, self._height)

        if QtGui.QPixmapCache.find(filename, image):
            scaled = self._qt4_scale(image)

            if scaled is not image:
                # The Qt cache is application wide so we only keep the last
                # size asked for.
                QtGui.QPixmapCache.remove(filename);
                QtGui.QPixmapCache.insert(filename, scaled)
        else:
            # Load the image from the file and add it to the cache.
            image.load(filename)
            scaled = self._qt4_scale(image)
            QtGui.QPixmapCache.insert(filename, scaled)

        return scaled

    # Qt doesn't distinguish between bitmaps and images.
    _tk_imagecache_get_bitmap = _tk_imagecache_get_image

    def _qt4_scale(self, image):
        """ Scales the given image if necessary. """

        # Although Qt won't scale the image if it doesn't need to, it will make
        # a deep copy which we don't need.
        if image.width() != self._width or image.height()!= self._height:
            image = image.scaled(self._width, self._height)

        return image
