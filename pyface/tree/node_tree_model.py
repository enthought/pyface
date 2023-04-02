# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The model for a tree control with extensible node types. """


from traits.api import Dict, Instance


from .node_manager import NodeManager
from .tree_model import TreeModel


class NodeTreeModel(TreeModel):
    """ The model for a tree control with extensible node types. """

    # 'NodeTreeModel' interface --------------------------------------------

    # The node manager looks after all node types.
    node_manager = Instance(NodeManager, ())

    # Private interface ----------------------------------------------------

    # Node monitors.
    _monitors = Dict()

    # ------------------------------------------------------------------------
    # 'TreeModel' interface.
    # ------------------------------------------------------------------------

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False.

        This method is provided in case the model has an efficient way to
        determine whether or not a node has any children without having to
        actually get the children themselves.

        """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        if node_type.allows_children(node):
            has_children = node_type.has_children(node)

        else:
            has_children = False

        return has_children

    def get_children(self, node):
        """ Returns the children of a node. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        # Does the node allow children (ie. a folder allows children, a file
        # does not)?
        if node_type.allows_children(node):
            # Get the node's children.
            children = node_type.get_children(node)

        else:
            children = []

        return children

    def get_default_action(self, node):
        """ Returns the default action for a node. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.get_default_action(node)

    def get_drag_value(self, node):
        """ Get the value that is dragged for a node.

        By default the drag value is the node itself.

        """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.get_drag_value(node)

    def can_drop(self, node, data):
        """ Returns True if a node allows an object to be dropped onto it. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.can_drop(node, data)

    def drop(self, node, data):
        """ Drops an object onto a node. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        node_type.drop(node, data)

    def get_image(self, node, selected, expanded):
        """ Returns the label image for a node.

        Return None (the default) if no image is required.

        """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.get_image(node, selected, expanded)

    def get_key(self, node):
        """ Generate a unique key for a node. """

        return self.node_manager.get_key(node)

    def get_selection_value(self, node):
        """ Get the value that is used when a node is selected.

        By default the selection value is the node itself.

        """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.get_selection_value(node)

    def get_text(self, node):
        """ Returns the label text for a node.

        Return None if no text is required.  By default we return 'str(node)'.

        """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.get_text(node)

    def can_set_text(self, node, text):
        """ Returns True if the node's label can be set. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.can_set_text(node, text)

    def set_text(self, node, text):
        """ Sets the label text for a node. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.set_text(node, text)

    def is_collapsible(self, node):
        """ Returns True if the node is collapsible, otherwise False. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.is_collapsible(node)

    def is_draggable(self, node):
        """ Returns True if the node is draggable, otherwise False. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.is_draggable(node)

    def is_editable(self, node):
        """ Returns True if the node is editable, otherwise False.

        If the node is editable, its text can be set via the UI.

        """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.is_editable(node)

    def is_expandable(self, node):
        """ Returns True if the node is expandanble, otherwise False. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.is_expandable(node)

    def add_listener(self, node):
        """ Adds a listener for changes to a node. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        # Create a monitor to listen for changes to the node.
        monitor = node_type.get_monitor(node)
        if monitor is not None:
            self._start_monitor(monitor)
            self._monitors[self.node_manager.get_key(node)] = monitor

    def remove_listener(self, node):
        """ Removes a listener for changes to a node. """

        key = self.node_manager.get_key(node)

        monitor = self._monitors.get(key)
        if monitor is not None:
            self._stop_monitor(monitor)
            del self._monitors[key]

        return

    # ------------------------------------------------------------------------
    # 'NodeTreeModel' interface.
    # ------------------------------------------------------------------------

    def get_context_menu(self, node):
        """ Returns the context menu for a node. """

        # Determine the node type for this node.
        node_type = self.node_manager.get_node_type(node)

        return node_type.get_context_menu(node)

    # ------------------------------------------------------------------------
    # 'Private' interface
    # ------------------------------------------------------------------------

    def _start_monitor(self, monitor):
        """ Starts a monitor. """

        monitor.observe(self._on_nodes_changed, "nodes_changed")

        monitor.observe(self._on_nodes_inserted, "nodes_inserted")

        monitor.observe(self._on_nodes_removed, "nodes_removed")

        monitor.observe(self._on_nodes_replaced, "nodes_replaced")

        monitor.observe(self._on_structure_changed, "structure_changed")

        monitor.start()

    def _stop_monitor(self, monitor):
        """ Stops a monitor. """

        monitor.observe(self._on_nodes_changed, "nodes_changed", remove=True)

        monitor.observe(self._on_nodes_inserted, "nodes_inserted", remove=True)

        monitor.observe(self._on_nodes_removed, "nodes_removed", remove=True)

        monitor.observe(self._on_nodes_replaced, "nodes_replaced", remove=True)

        monitor.observe(
            self._on_structure_changed, "structure_changed", remove=True
        )

        monitor.stop()

        return

    # Trait event handlers -------------------------------------------------

    # Static ----

    # fixme: Commented this out as listeners are added and removed by the tree.
    # This caused duplicate monitors to be created for the root node.
    ##     def _root_changed(self, old, new):
    ##         """ Called when the root of the model has been changed. """

    ##         if old is not None:
    ##             # Remove a listener for structure/appearance changes
    ##             self.remove_listener(old)

    ##         if new is not None:
    ##             # Wire up a listener for structure/appearance changes
    ##             self.add_listener(new)

    ##         return

    # Dynamic ----

    def _on_nodes_changed(self, event):
        """ Called when nodes have changed. """

        self.nodes_changed = event.new

    def _on_nodes_inserted(self, event):
        """ Called when nodes have been inserted. """

        self.nodes_inserted = event.new

    def _on_nodes_removed(self, event):
        """ Called when nodes have been removed. """

        self.nodes_removed = event.new

    def _on_nodes_replaced(self, event):
        """ Called when nodes have been replaced. """

        self.nodes_replaced = event.new

    def _on_structure_changed(self, event):
        """ Called when the structure of a node has changed drastically. """

        self.structure_changed = event.new

        return
