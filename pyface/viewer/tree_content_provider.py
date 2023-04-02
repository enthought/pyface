# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for tree content providers. """


from .content_provider import ContentProvider


class TreeContentProvider(ContentProvider):
    """ Abstract base class for tree content providers.

    Tree content providers are used by (surprise, surprise) tree viewers!

    """

    # ------------------------------------------------------------------------
    # 'ContentProvider' interface.
    # ------------------------------------------------------------------------

    def get_elements(self, element):
        """ Returns a list of the elements to display in a viewer.

        Returns a list of elements to display in a viewer when its (ie. the
        viewer's) input is set to the given element.

        The returned list should not be modified by the viewer.

        """

        return self.get_children(element)

    # ------------------------------------------------------------------------
    # 'TreeContentProvider' interface.
    # ------------------------------------------------------------------------

    def get_parent(self, element):
        """ Returns the parent of an element.

        Returns None if the element either has no parent (ie. it is the root of
        the tree), or if the parent cannot be computed.

        """

        return None

    def get_children(self, element):
        """ Returns the children of an element. """

        raise NotImplementedError()

    def has_children(self, element):
        """ Returns True iff the element has children, otherwise False. """

        raise NotImplementedError()
