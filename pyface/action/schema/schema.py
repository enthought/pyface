# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Schema class definitions

This module defines the Schema
"""

from traits.api import (
    Bool,
    Callable,
    Enum,
    HasTraits,
    Instance,
    List,
    Property,
    Str,
    Tuple,
    Union,
)

from pyface.util.id_helper import get_unique_id

# NOTE
# This module should never import directly or indirectly any toolkit-dependent
# code at the top level.  This permits it to be used declaratively in a
# toolkit-agnostic way if needed.

# Trait definitions.
SubSchema = Union(
    None,
    Instance("pyface.action.action.Action"),
    Instance("pyface.action.action_item.ActionItem"),
    Instance("pyface.action.group.Group"),
    Instance("pyface.action.menu_manager.MenuManager"),
    Instance("pyface.action.schema.schema.GroupSchema"),
    Instance("pyface.action.schema.schema.MenuSchema"),
    Instance("pyface.action.schema.schema.Schema"),
)


class Schema(HasTraits):
    """ The abstract base class for all action schemas.
    """

    #: The schema's identifier (unique within its parent schema).
    id = Str()

    #: The list of sub-items in the schema. These items can be other
    #: (non-top-level) schema or concrete instances from the Pyface API.
    items = List(SubSchema)

    def __init__(self, *items, **traits):
        """ Creates a new schema.
        """
        super().__init__(**traits)
        self.items.extend(items)

    def create(self, children):
        """ Create the appropriate pyface.action instance with the specified
            child items.
        """
        raise NotImplementedError()

    # Trait initializers ---------------------------------------------------

    def _id_default(self):
        return get_unique_id(self)


class ActionSchema(Schema):
    """ Action schema for Pyface Actions.

    An action schema cannot have children. It is used as an action factory
    to make sure a larger schema (e.g., a menu schema) can be used multiple
    times. Without using an ActionSchema, a reference to the action is added
    to every menu created from the schema. When one of the menus is destroyed,
    the action is also destroyed and is made unusable.
    """

    #: A factory for the Action instance.
    action_factory = Callable()

    #: Items is overwritten to be empty and read-only to avoid assigning to
    #: it by mistake.
    items = Property()

    def _get_items(self):
        return []

    def create(self, children):
        """ Create the appropriate Pyface Action instance. """

        traits = dict(id=self.id)
        return self.action_factory(**traits)

    # Trait initializers ---------------------------------------------------

    def _action_factory_default(self):
        from pyface.action.action import Action
        return Action


class GroupSchema(Schema):
    """ A schema for a Pyface Group.
    """

    #: A factory for instantiating a pyface Group.
    group_factory = Callable()

    #: Does the group require a separator when it is visualized?
    separator = Bool(True)

    def create(self, children):
        traits = dict(id=self.id, separator=self.separator)
        return self.group_factory(*children, **traits)

    # Trait initializers ---------------------------------------------------

    def _group_factory_default(self):
        from pyface.action.group import Group
        return Group


class MenuSchema(Schema):
    """ A schema for a Pyface MenuManager.
    """

    #: The menu's user visible name.
    name = Str()

    #: Does the menu require a separator before the menu item?
    separator = Bool(False)

    #: The default action for tool button when shown in a toolbar (Qt only)
    action = Instance("pyface.action.action.Action")

    #: A factory for instantiating a pyface MenuManager.
    menu_manager_factory = Callable()

    def create(self, children):
        traits = dict(id=self.id, name=self.name, separator=self.separator)
        if self.action:
            traits["action"] = self.action
        return self.menu_manager_factory(*children, **traits)

    # Trait initializers ---------------------------------------------------

    def _menu_manager_factory_default(self):
        from pyface.action.menu_manager import MenuManager
        return MenuManager


class MenuBarSchema(Schema):
    """ A schema for a Pyface MenuBarManager.
    """

    #: Assign a default ID for menu bar schemas.
    id = "MenuBar"

    #: A factory for instantiating a pyface MenuBarManager.
    menu_bar_manager_factory = Callable()

    def create(self, children):
        traits = dict(id=self.id)
        return self.menu_bar_manager_factory(*children, **traits)

    # Trait initializers ---------------------------------------------------

    def _menu_bar_manager_factory_default(self):
        from pyface.action.menu_bar_manager import MenuBarManager
        return MenuBarManager


class ToolBarSchema(Schema):
    """ A schema for a Pyface ToolBarManager.
    """

    #: Assign a default ID for tool bar schemas.
    id = "ToolBar"

    #: The tool bar's user visible name. Note that this name may not be used on
    #: all platforms.
    name = Str("Tool Bar")

    #: The size of tool images (width, height).
    image_size = Tuple((16, 16))

    #: The orientation of the toolbar.
    orientation = Enum("horizontal", "vertical")

    #: Should we display the horizontal divider?
    show_divider = Bool(True)

    #: Should we display the name of each tool bar tool under its image?
    show_tool_names = Bool(True)

    #: A factory for instantiating a pyface ToolBarManager
    tool_bar_manager_factory = Callable()

    def create(self, children):
        traits = dict(
            id=self.id,
            name=self.name,
            image_size=self.image_size,
            orientation=self.orientation,
            show_divider=self.show_divider,
            show_tool_names=self.show_tool_names,
        )
        return self.tool_bar_manager_factory(*children, **traits)

    # Trait initializers ---------------------------------------------------

    def _tool_bar_manager_factory_default(self):
        from pyface.action.tool_bar_manager import ToolBarManager
        return ToolBarManager


# Convenience abbreviations.
SGroup = GroupSchema
SMenu = MenuSchema
SMenuBar = MenuBarSchema
SToolBar = ToolBarSchema
