# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Filters for local file system viewers. """


from os.path import isdir


from pyface.viewer.api import ViewerFilter


class AllowOnlyFolders(ViewerFilter):
    """ A viewer filter that allows only folders (not files). """

    def select(self, viewer, parent, element):
        """ Returns True if the element is 'allowed' (ie. NOT filtered).

        'viewer'  is the viewer that we are filtering elements for.
        'parent'  is the parent element.
        'element' is the element to select.

        """

        return isdir(element)
