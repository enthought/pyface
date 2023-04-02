# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Base class for all sorters. """

from traits.api import HasTraits


class Sorter(HasTraits):
    """ Abstract base class for all sorters. """

    # ------------------------------------------------------------------------
    # 'ViewerSorter' interface.
    # ------------------------------------------------------------------------

    def sort(self, widget, parent, nodes):
        """ Sorts a list of nodes IN PLACE.

        'widget' is the widget that we are sorting nodes for.
        'parent' is the parent node.
        'nodes'  is the list of nodes to sort.

        Returns the list that was sorted IN PLACE (for convenience).

        """

        # This creates a comparison function with the names 'widget' and
        # 'parent' bound to the corresponding arguments to this method.
        def key(node):
            """ Comparator. """

            return self.key(widget, parent, node)

        nodes.sort(key=key)

        return nodes

    def key(self, widget, parent, node):
        category = self.category(widget, parent, node)
        text = widget.model.get_text(node)
        return (category, text)

    def category(self, widget, parent, node):
        """ Returns the category (an integer) for an node.

        'parent' is the parent node.
        'nodes'  is the node to return the category for.

        Categories are used to sort nodes into bins.  The bins are arranged in
        ascending numeric order.  The nodes within a bin are arranged as
        dictated by the sorter's 'compare' method.

        By default all nodes are given the same category (0).

        """

        return 0

    def is_sorter_trait(self, node, trait_name):
        """ Is the sorter affected by changes to a node's trait?

        'node'       is the node.
        'trait_name' is the name of the trait.

        Returns True if the sorter would be affected by changes to the trait
        named 'trait_name' on the specified node.

        By default we return False.

        """

        return False
