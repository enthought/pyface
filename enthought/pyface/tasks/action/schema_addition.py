# Enthought library imports.
from enthought.pyface.action.api import Action, ActionItem, Group, MenuManager
from enthought.traits.api import HasTraits, Str, Trait

# Trait definitions.
ActionElement = Trait(None, Action, ActionItem, Group, MenuManager)


class SchemaAddition(HasTraits):
    """ An addition to an existing menu bar or tool bar schema.
    """

    # The Pyface action/group/menu to insert.
    item = ActionElement

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
