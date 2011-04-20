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
""" Abstract base class for content providers. """


# Enthought library imports.
from traits.api import HasTraits


class ContentProvider(HasTraits):
    """ Abstract base class for content providers. """

    #########################################################################
    # 'ContentProvider' interface.
    #########################################################################

    def get_elements(self, element):
        """ Returns a list of the elements to display in a viewer.

        Returns a list of elements to display in a viewer when its (ie. the
        viewer's) input is set to the given element.

        The returned list should not be modified by the viewer.

        """

        raise NotImplementedError

#### EOF ####################################################################
