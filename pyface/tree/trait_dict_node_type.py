# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The node type for a trait dictionary. """


from traits.api import Any, Str


from .node_type import NodeType


class TraitDictNodeType(NodeType):
    """ The node type for a trait dictionary. """

    # 'TraitDictNodeType' interface ----------------------------------------

    # The type of object that provides the trait dictionary.
    klass = Any()

    # The label text.
    text = Str()

    # The trait name.
    trait_name = Str()

    # ------------------------------------------------------------------------
    # 'NodeType' interface.
    # ------------------------------------------------------------------------

    def is_type_for(self, node):
        """ Returns True if this node type recognizes a node. """

        is_type_for = (
            isinstance(node, dict)
            and hasattr(node, "object")
            and isinstance(node.object, self.klass)
            and node.name == self.trait_name
        )

        return is_type_for

    def allows_children(self, node):
        """ Does the node allow children (ie. a folder vs a file). """

        return True

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False. """

        return len(node) > 0

    def get_children(self, node):
        """ Returns the children of a node. """

        return list(node.values())

    def get_text(self, node):
        """ Returns the label text for a node. """

        return self.text
