# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A generic base-class for items in a tree data structure.

An example::

    root = TreeItem(data='Root')

    fruit = TreeItem(data='Fruit')
    fruit.append(TreeItem(data='Apple', allows_children=False))
    fruit.append(TreeItem(data='Orange', allows_children=False))
    fruit.append(TreeItem(data='Pear', allows_children=False))
    root.append(fruit)

    veg = TreeItem(data='Veg')
    veg.append(TreeItem(data='Carrot', allows_children=False))
    veg.append(TreeItem(data='Cauliflower', allows_children=False))
    veg.append(TreeItem(data='Sprout', allows_children=False))
    root.append(veg)

"""


from traits.api import Any, Bool, HasTraits, Instance, List, Property


class TreeItem(HasTraits):
    """ A generic base-class for items in a tree data structure. """

    # 'TreeItem' interface -------------------------------------------------

    # Does this item allow children?
    allows_children = Bool(True)

    # The item's children.
    children = List(Instance("TreeItem"))

    # Arbitrary data associated with the item.
    data = Any()

    # Does the item have any children?
    has_children = Property(Bool)

    # The item's parent.
    parent = Instance("TreeItem")

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __str__(self):
        """ Returns the informal string representation of the object. """

        if self.data is None:
            s = ""

        else:
            s = str(self.data)

        return s

    # ------------------------------------------------------------------------
    # 'TreeItem' interface.
    # ------------------------------------------------------------------------

    # Properties -----------------------------------------------------------

    # has_children
    def _get_has_children(self):
        """ True iff the item has children. """

        return len(self.children) != 0

    # Methods -------------------------------------------------------------#

    def append(self, child):
        """ Appends a child to this item.

        This removes the child from its current parent (if it has one).

        """

        return self.insert(len(self.children), child)

    def insert(self, index, child):
        """ Inserts a child into this item at the specified index.

        This removes the child from its current parent (if it has one).

        """

        if child.parent is not None:
            child.parent.remove(child)

        child.parent = self
        self.children.insert(index, child)

        return child

    def remove(self, child):
        """ Removes a child from this item. """

        child.parent = None
        self.children.remove(child)

        return child

    def insert_before(self, before, child):
        """ Inserts a child into this item before the specified item.

        This removes the child from its current parent (if it has one).

        """

        index = self.children.index(before)

        self.insert(index, child)

        return (index, child)

    def insert_after(self, after, child):
        """ Inserts a child into this item after the specified item.

        This removes the child from its current parent (if it has one).

        """

        index = self.children.index(after)

        self.insert(index + 1, child)

        return (index, child)
