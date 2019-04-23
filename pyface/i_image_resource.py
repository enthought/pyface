#------------------------------------------------------------------------------
# Copyright (c) 2005-2009 by Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------
""" The interface for an image resource. """

try:
    from collections.abc import Sequence
except ImportError:  # Python 3.8 deprecation
    from collections import Sequence

from pyface.resource_manager import resource_manager
from pyface.resource.resource_path import resource_module, resource_path
from traits.api import Interface, List, Unicode
import six


class IImageResource(Interface):
    """ The interface for an image resource.

    An image resource describes the location of an image and provides a way
    to create a toolkit-specific image on demand.
    """

    #### 'ImageResource' interface ############################################

    #: The absolute path to the image.
    absolute_path = Unicode

    #: The name of the image.
    name = Unicode

    #: A list of directories, classes or instances that will be used to search
    #: for the image (see the resource manager for more details).
    search_path = List

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, name, search_path=None):
        """ Creates a new image resource. """

    ###########################################################################
    # 'ImageResource' interface.
    ###########################################################################

    def create_image(self, size=None):
        """ Creates a toolkit specific image for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        image : toolkit image
            The toolkit image corresponding to the resource and the specified
            size.
        """

    # FIXME v3: The need to distinguish between bitmaps and images is toolkit
    # specific so, strictly speaking, the conversion to a bitmap should be done
    # wherever the toolkit actually needs it.
    def create_bitmap(self, size=None):
        """ Creates a toolkit specific bitmap for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        image : toolkit image
            The toolkit image corresponding to the resource and the specified
            size as a bitmap.
        """

    def create_icon(self, size=None):
        """ Creates a toolkit-specific icon for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        image : toolkit image
            The toolkit image corresponding to the resource and the specified
            size as an icon.
        """

    @classmethod
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



class MImageResource(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IImageResource interface.

    Implements: __init__(), create_image()
    """

    #### Private interface ####################################################

    #: The image-not-found image.  Note that it is not a trait.
    _image_not_found = None

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, name, search_path=None):
        self.name = name

        if isinstance(search_path, six.string_types):
            _path = [search_path]
        elif isinstance(search_path, Sequence):
            _path = search_path
        elif search_path is not None:
            _path = [search_path]
        else:
            _path = [resource_path()]
        self.search_path = _path + [resource_module()]

    ###########################################################################
    # 'ImageResource' interface.
    ###########################################################################

    def create_image(self, size=None):
        """ Creates a toolkit specific image for this resource.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        image : toolkit image
            The toolkit image corresponding to the resource and the specified
            size.
        """
        ref = self._get_ref(size)
        if ref is not None:
            image = ref.load()

        else:
            image = self._get_image_not_found_image()

        return image

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_ref(self, size=None):
        """ Return the resource manager reference to the image.

        Parameters
        ----------
        size : (int, int) or None
            The desired size as a width, height tuple, or None if wanting
            default image size.

        Returns
        -------
        ref : ImageReference instance
            The reference to the requested image.
        """

        if self._ref is None:
            self._ref = resource_manager.locate_image(self.name,
                    self.search_path, size)

        return self._ref

    def _get_image_not_found_image(self):
        """ Returns the 'image not found' image.

        Returns
        -------
        image : toolkit image
            The 'not found' toolkit image.
        """

        not_found = self._get_image_not_found()

        if self is not not_found:
            image = not_found.create_image()

        else:
            raise ValueError("cannot locate the file for 'image_not_found'")

        return image

    @classmethod
    def _get_image_not_found(cls):
        """ Returns the 'image not found' image resource.

        Returns
        -------
        not_found : ImageResource instance
            An image resource for the the 'not found' image.
        """

        if cls._image_not_found is None:
            from pyface.image_resource import ImageResource

            cls._image_not_found = ImageResource('image_not_found')

        return cls._image_not_found
