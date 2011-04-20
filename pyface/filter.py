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
""" Base class for all filters. """


# Enthought library imports.
from traits.api import HasPrivateTraits


class Filter(HasPrivateTraits):
    """ Abstract base class for all filters. """

    ###########################################################################
    # 'Filter' interface.
    ###########################################################################

    def filter(self, widget, parent, nodes):
        """ Filters a list of nodes.

        'widget'is the widget that we are filtering nodes for.
        'parent'is the parent node.
        'nodes' is the list of nodes to filter.

        Returns a list containing only those nodes for which 'select' returns
        True.

        """

        return [e for e in nodes if self.select(widget, parent, e)]

    def select(self, widget, parent, node):
        """ Returns True if the node is 'allowed' (ie. NOT filtered).

        'widget' is the widget that we are filtering nodes for.
        'parent' is the parent node.
        'node'   is the node to select.

        By default we return True.

        """

        return True

    def is_filter_trait(self, node, trait_name):
        """ Is the filter affected by changes to a node's trait?

        'node'       is the node.
        'trait_name' is the name of the trait.

        Returns True if the filter would be affected by changes to the trait
        named 'trait_name' on the specified node.

        By default we return False.

        """

        return False

#### EOF ######################################################################
