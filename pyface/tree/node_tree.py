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
""" A tree control with extensible node types. """


# Standard library imports.
import inspect

# Enthought library imports.
from pyface.action.api import ActionEvent
from traits.api import Instance, List, Property

# Local imports.
from .node_manager import NodeManager
from .node_type import NodeType
from .node_tree_model import NodeTreeModel
from .tree import Tree


class NodeTree(Tree):
    """ A tree control with extensible node types. """

    #### 'Tree' interface #####################################################

    # The model that provides the data for the tree.
    model = Instance(NodeTreeModel, ())

    #### 'NodeTree' interface #################################################

    # The node manager looks after all node types.
    node_manager = Property(Instance(NodeManager))

    # The node types in the tree.
    node_types = Property(List(NodeType))

    ###########################################################################
    # 'NodeTree' interface.
    ###########################################################################

    #### Properties ###########################################################

    # node_manager
    def _get_node_manager(self):
        """ Returns the root node of the tree. """

        return self.model.node_manager

    def _set_node_manager(self, node_manager):
        """ Sets the root node of the tree. """

        self.model.node_manager = node_manager

        return

    # node_types
    def _get_node_types(self):
        """ Returns the node types in the tree. """

        return self.model.node_manager.node_types

    def _set_node_types(self, node_types):
        """ Sets the node types in the tree. """

        self.model.node_manager.node_types = node_types

        return

    ###########################################################################
    # 'Tree' interface.
    ###########################################################################

    #### Trait event handlers #################################################

    def _node_activated_changed(self, obj):
        """ Called when a node has been activated (i.e., double-clicked). """

        default_action = self.model.get_default_action(obj)
        if default_action is not None:
            self._perform_default_action(default_action, obj)

        return

    def _node_right_clicked_changed(self, (obj, point)):
        """ Called when the right mouse button is clicked on the tree. """

        # Add the node that the right-click occurred on to the selection.
        self.select(obj)

        # fixme: This is a hack to allow us to attach the node that the
        # right-clicked occurred on to the action event.
        self._context = obj

        # Ask the model for the node's context menu.
        menu_manager = self.model.get_context_menu(obj)
        if menu_manager is not None:
            self._popup_menu(menu_manager, obj, point)

        return

    ###########################################################################
    # 'ActionController' interface.
    ###########################################################################

    def add_to_menu(self, menu_item):
        """ Adds a menu item to a menu bar. """

        pass

    def add_to_toolbar(self, toolvar_item):
        """ Adds a tool bar item to a tool bar. """

        pass

    def can_add_to_menu(self, action):
        """ Returns True iff an action can be added to the menu. """

        return True

    def perform(self, action, event):
        """ Perform an action. """

        # fixme: We need a more formal event structure!
        event.widget  = self
        event.context = self._context

        # fixme: the 'perform' method without taking an event is deprecated!
        args, varargs, varkw, defaults = inspect.getargspec(action.perform)

        # If the only argument is 'self' then this is the DEPRECATED
        # interface.
        if len(args) == 1:
            action.perform()

        else:
            action.perform(event)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_action_event(self, obj):
        """ Return a new action event for the specified object. """

        return ActionEvent(widget=self, context=obj)

    def _perform_default_action(self, action, obj):
        """ Perform the default action on the specified object. """

        action.perform(self._create_action_event(obj))

        return

    def _popup_menu(self, menu_manager, obj, point):
        """ Popup the menu described by the menu manager. """

        # Create the actual menu control.
        menu = menu_manager.create_menu(self.control, self)
        if not menu.is_empty():
            # Show the menu. If an action is selected it will be performed
            # *before* this call returns.
            menu.show(*point)

            # This gives the actions in the menu manager a chance to cleanup
            # any event listeners etc.
            menu_manager.destroy()

        return

#### EOF ######################################################################
