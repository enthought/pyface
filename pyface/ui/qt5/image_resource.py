#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

#
# Author: Riverbank Computing Limited
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------


# Standard library imports.
import os

# Major package imports.
from pyface.qt import QtGui

# Enthought library imports.
from traits.api import Any, HasTraits, List, Property, provides
from traits.api import Unicode

# Local imports.
from pyface.i_image_resource import IImageResource, MImageResource


@provides(IImageResource)
class ImageResource(MImageResource, HasTraits):
    """ The toolkit specific implementation of an ImageResource.  See the
    IImageResource interface for the API documentation.
    """


    #### Private interface ####################################################

    # The resource manager reference for the image.
    _ref = Any

    #### 'ImageResource' interface ############################################

    absolute_path = Property(Unicode)

    name = Unicode

    search_path = List

    ###########################################################################
    # 'ImageResource' interface.
    ###########################################################################

    # Qt doesn't specifically require bitmaps anywhere so just use images.
    create_bitmap = MImageResource.create_image

    def create_icon(self, size=None):
        ref = self._get_ref(size)

        if ref is not None:
            image = ref.load()
        else:
            image = self._get_image_not_found_image()

        return QtGui.QIcon(image)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_absolute_path(self):
        # FIXME: This doesn't quite work the new notion of image size. We
        # should find out who is actually using this trait, and for what!
        # (AboutDialog uses it to include the path name in some HTML.)
        ref = self._get_ref()
        if ref is not None:
            absolute_path = os.path.abspath(self._ref.filename)

        else:
            absolute_path = self._get_image_not_found().absolute_path

        return absolute_path

#### EOF ######################################################################
