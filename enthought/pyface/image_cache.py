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
""" An image cache. """


# Local imports.
from toolkit import patch_toolkit


class ImageCache:
    """ An image cache. """

    __tko__ = 'ImageCache'

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, width, height):
        """ Creates a new image cache. """

        patch_toolkit(self)

        self._width = width
        self._height = height

        self._tk_imagecache_init_cache()

        return

    ###########################################################################
    # 'ImageCache' interface.
    ###########################################################################

    def get_image(self, filename):
        """ Returns the specified image. """

        return self._tk_imagecache_get_image(filename)

    def get_bitmap(self, filename):
        """ Returns the specified image as a bitmap. """

        return self._tk_imagecache_get_bitmap(filename)

    ###########################################################################
    # 'ImageCache' toolkit interface.
    ###########################################################################

    def _tk_imagecache_init_cache(self):
        """ Initialise the cache. """

        pass

    def _tk_imagecache_get_image(self, filename):
        """ Returns the specified image.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_imagecache_get_bitmap(self, filename):
        """ Returns the specified image as a bitmap.
        
        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
