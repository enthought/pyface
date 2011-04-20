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
""" The interface for an image cache. """


# Enthought library imports.
from traits.api import Interface


class IImageCache(Interface):
    """ The interface for an image cache. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, width, height):
        """ Creates a new image cache for images of the given size. """

    ###########################################################################
    # 'ImageCache' interface.
    ###########################################################################

    def get_image(self, filename):
        """ Returns the specified image. """

    # FIXME v3: The need to distinguish between bitmaps and images is toolkit
    # specific so, strictly speaking, the conversion to a bitmap should be done
    # wherever the toolkit actually needs it.
    def get_bitmap(self, filename):
        """ Returns the specified image as a bitmap. """


class MImageCache(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IImageCache interface.
    """

#### EOF ######################################################################
