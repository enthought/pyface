# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for all viewer sorters. """


from traits.api import HasTraits


class ViewerSorter(HasTraits):
    """ Abstract base class for all viewer sorters. """

    # ------------------------------------------------------------------------
    # 'ViewerSorter' interface.
    # ------------------------------------------------------------------------

    def sort(self, viewer, parent, elements):
        """ Sorts a list of elements IN PLACE.

        'viewer'   is the viewer that we are sorting elements for.
        'parent'   is the parent element.
        'elements' is the list of elements to sort.

        Returns the list that was sorted IN PLACE (for convenience).

        """

        # This creates a comparison function with the names 'viewer' and
        # 'parent' bound to the corresponding arguments to this method.
        def key(element):
            """ Key function. """
            return self.key(viewer, parent, element)

        elements.sort(key=key)

        return elements

    def key(self, viewer, parent, element):
        """ Returns the result of comparing two elements.

        'viewer'    is the viewer that we are sorting elements for.
        'parent'    is the parent element.
        'element'   is the the first element being sorted.

        """

        # Get the category
        category = self.category(viewer, parent, element)

        # Get the label
        if hasattr(viewer, "label_provider"):
            label = viewer.label_provider.get_text(viewer, element)
        else:
            label = viewer.node_model.get_text(viewer, element)

        return (category, label)

    def category(self, viewer, parent, element):
        """ Returns the category (an integer) for an element.

        'parent'   is the parent element.
        'elements' is the element to return the category for.

        Categories are used to sort elements into bins.  The bins are
        arranged in ascending numeric order.  The elements within a bin
        are arranged as dictated by the sorter's 'compare' method.

        By default all elements are given the same category (0).

        """
        return 0

    def is_sorter_trait(self, element, trait_name):
        """ Is the sorter affected by changes to an element's trait?

        'element'    is the element.
        'trait_name' is the name of the trait.

        Returns True if the sorter would be affected by changes to the trait
        named 'trait_name' on the specified element.

        By default we return False.

        """
        return False
