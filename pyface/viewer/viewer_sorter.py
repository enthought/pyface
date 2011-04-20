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
""" Abstract base class for all viewer sorters. """


# Enthought library imports.
from traits.api import HasTraits


class ViewerSorter(HasTraits):
    """ Abstract base class for all viewer sorters. """

    ###########################################################################
    # 'ViewerSorter' interface.
    ###########################################################################

    def sort(self, viewer, parent, elements):
        """ Sorts a list of elements IN PLACE.

        'viewer'   is the viewer that we are sorting elements for.
        'parent'   is the parent element.
        'elements' is the list of elements to sort.

        Returns the list that was sorted IN PLACE (for convenience).

        """

        # This creates a comparison function with the names 'viewer' and
        # 'parent' bound to the corresponding arguments to this method.
        def comparator(element_a, element_b):
            """ Comparator. """

            return self.compare(viewer, parent, element_a, element_b)

        elements.sort(comparator)

        return elements

    def compare(self, viewer, parent, element_a, element_b):
        """ Returns the result of comparing two elements.

        'viewer'    is the viewer that we are sorting elements for.
        'parent'    is the parent element.
        'element_a' is the the first element to compare.
        'element_b' is the the second element to compare.

        """

        # Get the category for each element.
        category_a = self.category(viewer, parent, element_a)
        category_b = self.category(viewer, parent, element_b)

        # If they are not in the same category then return the result of
        # comparing the categories.
        if category_a != category_b:
            result = cmp(category_a, category_b)

        else:
            # Get the label text for each element.
            #
            # fixme: This is a hack until we decide whethwe we like the
            # JFace(ish) or Swing(ish) models!
            if hasattr(viewer, 'label_provider'):
              label_a = viewer.label_provider.get_text(viewer, element_a)
              label_b = viewer.label_provider.get_text(viewer, element_b)

            else:
                label_a = viewer.node_model.get_text(viewer, element_a)
                label_b = viewer.node_model.get_text(viewer, element_b)

            # Compare the label text.
            result = cmp(label_a, label_b)

        return result

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

#### EOF ######################################################################
