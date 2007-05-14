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


class ImageResource_wx(object):
    """ The ImageResource monkey patch for wx. """

    ###########################################################################
    # 'ImageResource' toolkit interface.
    ###########################################################################

    def _tk_imageresource_convert_to_bitmap(self, image):
        """ Convert a toolkit specific image to a toolkit specific bitmap. """

        return image.ConvertToBitmap()
    
    def _tk_imageresource_convert_to_icon(self, image):
        """ Convert a toolkit specific image to a toolkit specific icon. """

        # We have to convert the image to a bitmap first and then create an
        # icon from that.
        bmp = image.ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(bmp)

        return icon

    def _tk_imageresource_load_icon(self, ref):
        """ Load an icon for a resource. """

        # This assumes that the file is in an icon file (i.e. it has the '.ico'
        # extension).
        return wx.Icon(self.absolute_path, wx.BITMAP_TYPE_ICO)

#### EOF ######################################################################
