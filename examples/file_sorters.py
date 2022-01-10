# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Sorters for local file system viewers. """


from os.path import isdir


from pyface.viewer.api import ViewerSorter


class FileSorter(ViewerSorter):
    """ A sorter that arranges folders before files. """

    def category(self, viewer, parent, element):
        """ Returns the category (an integer) for an element.

        'parent'   is the parent element.
        'elements' is the element to return the category for.

        Categories are used to sort elements into bins.  The bins are
        arranged in ascending numeric order.  The elements within a bin
        are arranged as dictated by the sorter's 'compare' method.

        """

        if isdir(element):
            category = 0

        else:
            category = 1

        return category
