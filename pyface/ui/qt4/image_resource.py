# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
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


import os


from pyface.qt import QtGui


from traits.api import Any, HasTraits, List, Property, provides
from traits.api import Str


from pyface.i_image_resource import IImageResource, MImageResource


@provides(IImageResource)
class ImageResource(MImageResource, HasTraits):
    """ The toolkit specific implementation of an ImageResource.  See the
    IImageResource interface for the API documentation.
    """

    # Private interface ----------------------------------------------------

    # The resource manager reference for the image.
    _ref = Any()

    # 'ImageResource' interface --------------------------------------------

    absolute_path = Property(Str)

    name = Str()

    search_path = List()

    # ------------------------------------------------------------------------
    # 'IImage' interface.
    # ------------------------------------------------------------------------

    # Qt doesn't specifically require bitmaps anywhere so just use images.
    create_bitmap = MImageResource.create_image

    def create_icon(self, size=None):
        ref = self._get_ref(size)

        if ref is not None:
            image = ref.load()
        else:
            image = self._get_image_not_found_image()

        return QtGui.QIcon(image)

    def image_size(cls, image):
        """ Get the size of a toolkit image

        Parameters
        ----------
        image : toolkit image
            A toolkit image to compute the size of.

        Returns
        -------
        size : tuple
            The (width, height) tuple giving the size of the image.
        """
        size = image.size()
        return (size.width(), size.height())

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

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
