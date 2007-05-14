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
""" An image resource. """


# Standard library imports.
import os

# Enthought library imports.
from enthought.resource.resource_path import resource_path
from enthought.traits.api import Any, HasTraits, List, Property, Str

# Local imports.
from resource_manager import resource_manager
from toolkit import patch_toolkit


class ImageResource(HasTraits):
    """ An image resource.

    An image resource describes the location of an image and provides a way
    to create a toolkit-specific image on demand.
    """

    __tko__ = 'ImageResource'

    #### 'ImageResource' interface ############################################

    # The absolute path to the image.
    absolute_path = Property(Str)

    # The name of the image.
    name = Str

    # A list of directories, classes or instances that will be used to search
    # for the image (see the resource manager for more details).
    search_path = List

    #### Private interface ####################################################

    # The resource manager reference for the image.
    _ref = Any

    # The image-not-found image.  It is created as part of the lazy
    # initialisation.
    _image_not_found = None
    
    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, name, search_path=None):
        """ Creates a new image resource. """

        self._lazy_init_done = False

        self.name = name

        if search_path is not None:
            self.search_path = search_path

        else:
            self.search_path = [resource_path()]

        return

    ###########################################################################
    # 'ImageResource' interface.
    ###########################################################################

    #### Properties ###########################################################

    def _get_absolute_path(self):
        """ Returns the absolute path to the image. """

        # fixme: This doesn't quite wotk the new notion of image size. We
        # should find out who is actually using this trait, and for what!
        ref = self._get_ref()
        if ref is not None:
            absolute_path = os.path.abspath(self._ref.filename)

        else:
            self._lazy_init()

            absolute_path = self._image_not_found.absolute_path
            
        return absolute_path
    
    #### Methods ##############################################################
    
    def create_image(self, size=None):
        """ Creates a toolkit specific image for this resource. """

        self._lazy_init()

        ref = self._get_ref(size)
        if ref is not None:
            image = ref.load()

        else:
            image = self._get_image_not_found_image()
            
        return image

    def create_bitmap(self, size=None):
        """ Creates a toolkit specific bitmap for this resource. """

        self._lazy_init()

        ref = self._get_ref(size)
        if ref is not None:
            image = ref.load()

        else:
            image = self._get_image_not_found_image()

        return self._tk_imageresource_convert_to_bitmap(image)

    def create_icon(self, size=None):
        """ Creates a toolkit-specific icon for this resource. """

        self._lazy_init()

        ref = self._get_ref(size)
        if ref is not None:
            icon = self._tk_imageresource_load_icon(ref)

        else:
            image = self._get_image_not_found_image()
            icon = self._tk_imageresource_convert_to_icon(image)

        return icon

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_ref(self, size=None):
        """ Return the resource manager reference to the image. """

        if self._ref is None:
            self._ref = resource_manager.locate_image(
                self.name, self.search_path, size
            )

        return self._ref

    def _get_image_not_found_image(self):
        """ Returns the 'image not found' image. """

        if self is not self._image_not_found:
            image = self._image_not_found.create_image()

        # If we can't find the 'image not found' image then the installer must
        # be broken!
        else:
            raise ValueError("Rick's installer is broken")

        return image

    def _lazy_init(self):
        """ Do any post toolkit selection initialisation. """

        if self._lazy_init_done:
            return

        self._lazy_init_done = True

        patch_toolkit(self)

        if ImageResource._image_not_found is None:
            ImageResource._image_not_found = ImageResource('image_not_found')

    ###########################################################################
    # 'ImageResource' toolkit interface.
    ###########################################################################

    def _tk_imageresource_convert_to_bitmap(self, image):
        """ Convert a toolkit specific image to a toolkit specific bitmap.

        This must be reimplemented.
        """

        raise NotImplementedError
    
    def _tk_imageresource_convert_to_icon(self, image):
        """ Convert a toolkit specific image to a toolkit specific icon.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_imageresource_load_icon(self, ref):
        """ Load an icon for a resource.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
