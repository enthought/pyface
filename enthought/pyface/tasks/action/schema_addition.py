# Enthought library imports.
from enthought.traits.api import Callable, HasTraits, Str, Trait


class SchemaAddition(HasTraits):
    """ An addition to an existing menu bar or tool bar schema.
    """

    # The schema addition's identifier. This optional, but if left unspecified,
    # other schema additions will be unable to refer to this one.
    id = Str

    # A callable to create the item. Should have the following signature:
    #    callable() -> Action | ActionItem | Group | MenuManager | 
    #                  GroupSchema | MenuSchema
    # If the result is a schema, it will itself admit of extension by other
    # additions. If not, the result will be fixed.
    factory = Callable

    # A forward-slash-separated path through the action hierarchy to the menu
    # to add the action, group or menu to. For example:
    # - To add an item to the menu bar: ``path = "MenuBar"``
    # - To add an item to the tool bar: ``path = "ToolBar"``
    # - To add an item to a sub-menu: ``path = "MenuBar/File/New"``
    path = Str

    # The item appears after the item with this ID.
    # - for groups, this is the ID of another group.
    # - for menus and actions, this is the ID of another menu or action.
    after = Str

    # The action appears before the item with this ID.
    # - for groups, this is the ID of another group.
    # - for menus and actions, this is the ID of another menu or action.
    before = Str
