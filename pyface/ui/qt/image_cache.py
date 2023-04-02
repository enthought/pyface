# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


from pyface.qt import QtGui


from traits.api import HasTraits, provides


from pyface.i_image_cache import IImageCache, MImageCache


@provides(IImageCache)
class ImageCache(MImageCache, HasTraits):
    """ The toolkit specific implementation of an ImageCache.  See the
    IImageCache interface for the API documentation.
    """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, width, height):
        self._width = width
        self._height = height

    # ------------------------------------------------------------------------
    # 'ImageCache' interface.
    # ------------------------------------------------------------------------

    def get_image(self, filename):
        image = QtGui.QPixmapCache.find(filename)

        if image is not None:
            scaled = self._qt4_scale(image)

            if scaled is not image:
                # The Qt cache is application wide so we only keep the last
                # size asked for.
                QtGui.QPixmapCache.remove(filename)
                QtGui.QPixmapCache.insert(filename, scaled)
        else:
            # Load the image from the file and add it to the cache.
            image = QtGui.QPixmap(filename)
            scaled = self._qt4_scale(image)
            QtGui.QPixmapCache.insert(filename, scaled)

        return scaled

    # Qt doesn't distinguish between bitmaps and images.
    get_bitmap = get_image

    # ------------------------------------------------------------------------
    # Private 'ImageCache' interface.
    # ------------------------------------------------------------------------

    def _qt4_scale(self, image):
        """ Scales the given image if necessary. """

        # Although Qt won't scale the image if it doesn't need to, it will make
        # a deep copy which we don't need.
        if image.width() != self._width or image.height() != self._height:
            image = image.scaled(self._width, self._height)

        return image
