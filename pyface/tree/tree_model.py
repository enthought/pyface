# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Model for tree views. """


from traits.api import Any, HasTraits, Event


from .node_event import NodeEvent


class TreeModel(HasTraits):
    """ Model for tree views. """

    # 'TreeModel' interface ------------------------------------------------

    # The root of the model.
    root = Any()

    # Fired when nodes in the tree have changed in some way that affects their
    # appearance but NOT their structure or position in the tree.
    nodes_changed = Event(NodeEvent)

    # Fired when nodes have been inserted into the tree.
    nodes_inserted = Event(NodeEvent)

    # Fired when nodes have been removed from the tree.
    nodes_removed = Event(NodeEvent)

    # Fired when nodes have been replaced in the tree.
    nodes_replaced = Event(NodeEvent)

    # Fire when the structure of the tree has changed DRASTICALLY from a given
    # node down.
    structure_changed = Event(NodeEvent)

    # ------------------------------------------------------------------------
    # 'TreeModel' interface.
    # ------------------------------------------------------------------------

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False.

        This method is provided in case the model has an efficient way to
        determine whether or not a node has any children without having to
        actually get the children themselves.

        """

        raise NotImplementedError()

    def get_children(self, node):
        """ Returns the children of a node. """

        raise NotImplementedError()

    def get_drag_value(self, node):
        """ Get the value that is dragged for a node.

        By default the drag value is the node itself.

        """

        return node

    def can_drop(self, node, obj):
        """ Returns True if a node allows an object to be dropped onto it. """

        return False

    def drop(self, node, obj):
        """ Drops an object onto a node. """

        raise NotImplementedError()

    def get_image(self, node, selected, expanded):
        """ Returns the label image for a node.

        Return None (the default) if no image is required.

        """

        return None

    def get_key(self, node):
        """ Generate a unique key for a node. """

        try:
            key = hash(node)

        except:
            key = id(node)

        return key

    def get_selection_value(self, node):
        """ Get the value that is used when a node is selected.

        By default the selection value is the node itself.

        """

        return node

    def get_text(self, node):
        """ Returns the label text for a node.

        Return None if no text is required.  By default we return 'str(node)'.

        """

        return str(node)

    def can_set_text(self, node, text):
        """ Returns True if the node's label can be set. """

        return len(text.strip()) > 0

    def set_text(self, node, text):
        """ Sets the label text for a node. """

        pass

    def is_collapsible(self, node):
        """ Returns True if the node is collapsible, otherwise False. """

        return True

    def is_draggable(self, node):
        """ Returns True if the node is draggable, otherwise False. """

        return True

    def is_editable(self, node):
        """ Returns True if the node is editable, otherwise False.

        If the node is editable, its text can be set via the UI.

        """

        return False

    def is_expandable(self, node):
        """ Returns True if the node is expandanble, otherwise False. """

        return True

    def add_listener(self, node):
        """ Adds a listener for changes to a node. """

        pass

    def remove_listener(self, node):
        """ Removes a listener for changes to a node. """

        pass

    def fire_nodes_changed(self, node, children):
        """ Fires the nodes changed event. """

        self.nodes_changed = NodeEvent(node=node, children=children)

    def fire_nodes_inserted(self, node, children):
        """ Fires the nodes inserted event. """

        self.nodes_inserted = NodeEvent(node=node, children=children)

    def fire_nodes_removed(self, node, children):
        """ Fires the nodes removed event. """

        self.nodes_removed = NodeEvent(node=node, children=children)

    def fire_nodes_replaced(self, node, old_children, new_children):
        """ Fires the nodes removed event. """

        self.nodes_replaced = NodeEvent(
            node=node, old_children=old_children, children=new_children
        )

    def fire_structure_changed(self, node):
        """ Fires the structure changed event. """

        self.structure_changed = NodeEvent(node=node)

        return
