# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for an image cache. """


from traits.api import HasTraits, Interface


class IImageCache(Interface):
    """ The interface for an image cache. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, width, height):
        """ Creates a new image cache for images of the given size.

        Parameters
        ----------
        width : int
            The width of the images in pixels
        height : int
            The height of the images in pixels
        """

    # ------------------------------------------------------------------------
    # 'ImageCache' interface.
    # ------------------------------------------------------------------------

    def get_image(self, filename):
        """ Returns the scaled image specified.

        Parameters
        ----------
        filename : str
            The name of the file containing the image.

        Returns
        -------
        scaled : toolkit image
            The image referred to in the file, scaled to the cache's width
            and height.
        """

    # FIXME v3: The need to distinguish between bitmaps and images is toolkit
    # specific so, strictly speaking, the conversion to a bitmap should be done
    # wherever the toolkit actually needs it.
    def get_bitmap(self, filename):
        """ Returns the scaled image specified as a bitmap.

        Parameters
        ----------
        filename : str
            The name of the file containing the image.

        Returns
        -------
        scaled : toolkit bitmap
            The image referred to in the file, scaled to the cache's width
            and height, as a bitmap.
        """


class MImageCache(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IImageCache interface.
    """
