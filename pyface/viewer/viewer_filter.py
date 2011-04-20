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
""" Abstract base class for all viewer filters. """


# Enthought library imports.
from traits.api import HasTraits


class ViewerFilter(HasTraits):
    """ Abstract base class for all viewer filters. """

    ###########################################################################
    # 'ViewerFilter' interface.
    ###########################################################################

    def filter(self, viewer, parent, elements):
        """ Filters a list of elements.

        'viewer'   is the viewer that we are filtering elements for.
        'parent'   is the parent element.
        'elements' is the list of elements to filter.

        Returns a list containing only those elements for which 'select'
        returns True.

        """

        return [e for e in elements if self.select(viewer, parent, e)]

    def select(self, viewer, parent, element):
        """ Returns True if the element is 'allowed' (ie. NOT filtered).

        'viewer'  is the viewer that we are filtering elements for.
        'parent'  is the parent element.
        'element' is the element to select.

        By default we return True.

        """

        return True

    def is_filter_trait(self, element, trait_name):
        """ Is the filter affected by changes to an element's trait?

        'element'    is the element.
        'trait_name' is the name of the trait.

        Returns True if the filter would be affected by changes to the trait
        named 'trait_name' on the specified element.

        By default we return False.

        """

        return False

#### EOF ######################################################################
