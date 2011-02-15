# Enthought library imports.
from enthought.pyface.action.api import Action, ActionItem, Group, \
     MenuManager, MenuBarManager, ToolBarManager
from enthought.traits.api import Bool, Callable, HasTraits, Instance, List, \
     Str, Trait, Unicode

# Trait definitions.
SubSchema = Trait(None, Action, ActionItem, Group, MenuManager,
                  Instance('enthought.pyface.tasks.action.schema.GroupSchema'),
                  Instance('enthought.pyface.tasks.action.schema.MenuSchema'))


class Schema(HasTraits):
    """ The abstract base class for all Tasks action schemas.
    """

    # The schema's identifier (unique within its parent schema).
    id = Str

    # The list of sub-items in the schema. These items can be other
    # (non-top-level) schema or concrete instances from the Pyface API.
    items = List(SubSchema)

    def __init__(self, *items, **traits):
        """ Creates a new schema.
        """
        super(Schema, self).__init__(**traits)
        self.items.extend(items)

    def create(self, children):
        """ Create the appropriate pyface.action instance with the specified
            child items.
        """
        raise NotImplementedError


class GroupSchema(Schema):
    """ A schema for a Pyface Group.
    """

    # A factory for instantiating a pyface Group.
    group_factory = Callable(Group)

    # Does the group require a separator when it is visualized?
    separator = Bool(True)

    def create(self, children):
        traits = dict(id=self.id, separator=self.separator)
        return self.group_factory(*children, **traits)


class MenuSchema(Schema):
    """ A schema for a Pyface MenuManager.
    """

    # A factory for instantiating a pyface MenuManager.
    menu_manager_factory = Callable(MenuManager)

    # The menu's user visible name.
    name = Unicode

    def create(self, children):
        traits = dict(id=self.id, name=self.name)
        return self.menu_manager_factory(*children, **traits)


class MenuBarSchema(Schema):
    """ A schema for a Pyface MenuBarManager.
    """

    # Assign a default ID for menu bar schemas.
    id = 'MenuBar'

    # A factory for instantiating a pyface MenuBarManager.
    menu_bar_manager_factory = Callable(MenuBarManager)

    def create(self, children):
        traits = dict(id=self.id)
        return self.menu_bar_manager_factory(*children, **traits)


class ToolBarSchema(Schema):
    """ A schema for a Pyface ToolBarManager.
    """

    # Assign a default ID for tool bar schemas.
    id = 'ToolBar'

    # A factory for instantiating a pyfce ToolBarManager
    tool_bar_manager_factory = Callable(ToolBarManager)

    def create(self, children):
        traits = dict(id=self.id)
        return self.tool_bar_manager_factory(*children, **traits)


# Convenience abbreviations.
SGroup = GroupSchema
SMenu = MenuSchema
SMenuBar = MenuBarSchema
SToolBar = ToolBarSchema
