#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class ImageResource_qt4(object):
    """ The ImageResource monkey patch for Qt4. """

    ###########################################################################
    # 'ImageResource' toolkit interface.
    ###########################################################################

    def _tk_imageresource_convert_to_bitmap(self, image):
        """ Convert a toolkit specific image to a toolkit specific bitmap. """

        # Qt doesn't specifically require bitmaps anywhere so just return the
        # image as it is.
        return image
    
    def _tk_imageresource_convert_to_icon(self, image):
        """ Convert a toolkit specific image to a toolkit specific icon. """

        return QtGui.QIcon(image)

    def _tk_imageresource_load_icon(self, ref):
        """ Load an icon for a resource. """

        return QtGui.QIcon(ref.load())
