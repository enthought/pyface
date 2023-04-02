# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The default tree content provider. """


from .tree_content_provider import TreeContentProvider
from .tree_item import TreeItem


class DefaultTreeContentProvider(TreeContentProvider):
    """ The default tree content provider. """

    # ------------------------------------------------------------------------
    # 'TreeContentProvider' interface.
    # ------------------------------------------------------------------------

    def get_parent(self, item):
        """ Returns the parent of an item. """

        return item.parent

    def get_children(self, item):
        """ Returns the children of an item. """

        return item.children

    def has_children(self, item):
        """ True iff the item has children. """

        return item.has_children

    # ------------------------------------------------------------------------
    # 'DefaultTreeContentProvider' interface.
    # ------------------------------------------------------------------------

    def append(self, parent, child):
        """ Appends 'child' to the 'parent' item. """

        return self.insert(parent, len(parent.children), child)

    def insert_before(self, parent, before, child):
        """ Inserts 'child' into 'parent' item before 'before'. """

        index, child = parent.insert_before(before, child)

        return (index, child)

    def insert(self, parent, index, child):
        """ Inserts 'child' into the 'parent' item at 'index'. """

        parent.insert(index, child)

        return child

    def remove(self, parent, child):
        """ Removes 'child' from the 'parent' item. """

        parent.remove(child)

        return child

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _create_item(self, **kw):
        """ Creates a new item. """

        return TreeItem(**kw)
