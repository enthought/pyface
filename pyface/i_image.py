# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The base interface for an image. """
from traits.api import Interface


class IImage(Interface):
    """ The base interface for an image.

    This provides the interface specification that different types of image
    classes need to provide to be used by Pyface.
    """

    def create_image(self, size=None):
        """ Creates a toolkit specific image for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.  This is a *preferred* size and concrete
            implementations may or may not return an image of the precise
            size requested (indeed, this may be ignored).

        Returns
        -------
        image : toolkit image
            The toolkit image corresponding to the resource and the specified
            size.
        """

    def create_bitmap(self, size=None):
        """ Creates a toolkit specific bitmap image for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.  This is a *preferred* size and concrete
            implementations may or may not return an image of the precise
            size requested (indeed, this may be ignored).

        Returns
        -------
        image : toolkit bitmap
            The toolkit bitmap corresponding to the resource and the specified
            size.
        """

    def create_icon(self, size=None):
        """ Creates a toolkit-specific icon for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default icon size.  This is a *preferred* size and concrete
            implementations may or may not return an icon of the precise
            size requested (indeed, this may be ignored).

        Returns
        -------
        image : toolkit icon
            The toolkit image corresponding to the resource and the specified
            size as an icon.
        """
