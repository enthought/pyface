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
""" A shared resource manager for Pyface. """


# Enthought library imports.
from enthought.resource.api import ResourceFactory, ResourceManager

# Local imports.
from toolkit import patch_toolkit


class PyfaceResourceFactory(ResourceFactory):
    """ Creates resources. """

    __tko__ = 'PyfaceResourceFactory'

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self):
        """ Creates a new resource factory. """

        self._lazy_init_done = False

        return
    
    ###########################################################################
    # 'ResourceFactory' interface.
    ###########################################################################

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        self._lazy_init()

        return self._tk_pyfaceresourcefactory_image_from_file(filename)

    def image_from_data(self, data):
        """ Creates an image from the specified data. """

        self._lazy_init()

        return self._tk_pyfaceresourcefactory_image_from_data(data)

    ###########################################################################
    # Private 'PyfaceResourceFactory' interface.
    ###########################################################################

    def _lazy_init(self):
        """ Do any post toolkit selection initialisation. """

        if self._lazy_init_done:
            return

        self._lazy_init_done = True

        patch_toolkit(self)

    ###########################################################################
    # 'PyfaceResourceFactory' toolkit interface.
    ###########################################################################

    def _tk_pyfaceresourcefactory_image_from_file(self, filename):
        """ Creates an image from the data in the specified filename.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_pyfaceresourcefactory_image_from_data(self, data):
        """ Creates an image from the specified data.

        This must be reimplemented.
        """

        raise NotImplementedError

# A shared instance.
resource_manager = ResourceManager(
    resource_factory = PyfaceResourceFactory()
)

#### EOF ######################################################################
