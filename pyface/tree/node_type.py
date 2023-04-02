# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The base class for all node types. """


from traits.api import Any, HasPrivateTraits, Instance

from pyface.api import Image, ImageResource
from pyface.action.api import Action, Group
from pyface.action.api import MenuManager


class NodeType(HasPrivateTraits):
    """ The base class for all node types. """

    # The default image used to represent nodes that DO NOT allow children.
    DOCUMENT = ImageResource("document")

    # The default image used to represent nodes that allow children and are NOT
    # expanded.
    CLOSED_FOLDER = ImageResource("closed_folder")

    # The default image used to represent nodes that allow children and ARE
    # expanded.
    OPEN_FOLDER = ImageResource("open_folder")

    # 'NodeType' interface -------------------------------------------------

    # The node manager that the type belongs to.
    node_manager = Instance("pyface.tree.node_manager.NodeManager")

    # The image used to represent nodes that DO NOT allow children.
    image = Image(DOCUMENT)

    # The image used to represent nodes that allow children and are NOT
    # expanded.
    closed_image = Image(CLOSED_FOLDER)

    # The image used to represent nodes that allow children and ARE expanded.
    open_image = Image(OPEN_FOLDER)

    # The default actions/groups/menus available on nodes of this type (shown
    # on the context menu).
    actions = Any  # List

    # The default action for nodes of this type.  The default action is
    # performed when a node is activated (i.e., double-clicked).
    default_action = Instance(Action)

    # The default actions/groups/menus for creating new children within nodes
    # of this type (shown in the 'New' menu of the context menu).
    new_actions = Any  # List

    # ------------------------------------------------------------------------
    # 'NodeType' interface.
    # ------------------------------------------------------------------------

    # These methods are specific to the 'NodeType' interface ---------------

    def is_type_for(self, node):
        """ Returns True if a node is deemed to be of this type. """

        raise NotImplementedError()

    def allows_children(self, node):
        """ Does the node allow children (ie. a folder vs a file). """

        return False

    def get_actions(self, node):
        """ Returns the node-specific actions for a node. """

        return self.actions

    def get_context_menu(self, node):
        """ Returns the context menu for a node. """

        sat = Group(id="SystemActionsTop")
        nsa = Group(id="NodeSpecificActions")
        sab = Group(id="SystemActionsBottom")

        # The 'New' menu.
        new_actions = self.get_new_actions(node)
        if new_actions is not None and len(new_actions) > 0:
            sat.append(MenuManager(name="New", *new_actions))

        # Node-specific actions.
        actions = self.get_actions(node)
        if actions is not None and len(actions) > 0:
            for item in actions:
                nsa.append(item)

        # System actions (actions available on ALL nodes).
        system_actions = self.node_manager.system_actions
        if len(system_actions) > 0:
            for item in system_actions:
                sab.append(item)

        context_menu = MenuManager(sat, nsa, sab)
        context_menu.dump()

        return context_menu

    def get_copy_value(self, node):
        """ Get the value that is copied for a node.

        By default, returns the node itself.

        """

        return node

    def get_default_action(self, node):
        """ Returns the default action for a node. """

        return self.default_action

    def get_new_actions(self, node):
        """ Returns the new actions for a node. """

        return self.new_actions

    def get_paste_value(self, node):
        """ Get the value that is pasted for a node.

        By default, returns the node itself.

        """

        return node

    def get_monitor(self, node):
        """ Returns a monitor that detects changes to a node.

        Returns None by default,  which indicates that the node is not
        monitored.

        """

        return None

    # These methods are exactly the same as the 'TreeModel' interface -----#

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False.

        You only need to implement this method if children are allowed for the
        node (ie. 'allows_children' returns True).

        """

        return False

    def get_children(self, node):
        """ Returns the children of a node.

        You only need to implement this method if children are allowed for the
        node.

        """

        raise NotImplementedError()

    def get_drag_value(self, node):
        """ Get the value that is dragged for a node.

        By default, returns the node itself.

        """

        return node

    def can_drop(self, node, data):
        """ Returns True if a node allows an object to be dropped onto it. """

        return False

    def drop(self, obj, data):
        """ Drops an object onto a node. """

        raise NotImplementedError()

    def get_image(self, node, selected, expanded):
        """ Returns the label image for a node. """

        if self.allows_children(node):
            if expanded:
                order = ["open_image", "closed_image", "image"]
                default = self.OPEN_FOLDER

            else:
                order = ["closed_image", "open_image", "image"]
                default = self.CLOSED_FOLDER

        else:
            order = ["image", "open_image", "closed_image"]
            default = self.DOCUMENT

        # Use the search order to look for a trait that is NOT None.
        for name in order:
            image = getattr(self, name)
            if image is not None:
                break

        # If no such trait is found then use the default image.
        else:
            image = default

        return image

    def get_selection_value(self, node):
        """ Get the value that is used when a node is selected.

        By default the selection value is the node itself.

        """

        return node

    def get_text(self, node):
        """ Returns the label text for a node. """

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
        """ Returns True if the node is draggablee, otherwise False. """

        return True

    def can_rename(self, node):
        """ Returns True if the node can be renamed, otherwise False. """

        return False

    def is_editable(self, node):
        """ Returns True if the node is editable, otherwise False.

        If the node is editable, its text can be set via the UI.

        DEPRECATED: Use 'can_rename'.

        """

        return self.can_rename(node)

    def is_expandable(self, node):
        """ Returns True if the node is expandanble, otherwise False. """

        return True
