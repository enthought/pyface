# Enthought library imports.
from enthought.traits.api import Any, HasStrictTraits, List, Trait, Str

# Trait definitions.
NestedListStr = List(Trait(None, Str, List(Str)))


class TaskLayout(HasStrictTraits):
    """ A picklable object that describes the layout of a Task's dock panes.
    """

    # Lists of (possibly singly-nested) DockPane IDs. For the left and right
    # areas, dock panes are added from top to bottom; for the top and bottom
    # areas, dock panes are added from left to right. A nested list indicates a
    # tabbed pane group.
    left_panes = NestedListStr
    right_panes = NestedListStr
    bottom_panes = NestedListStr
    top_panes = NestedListStr

    # A toolkit-specific state object which encodes the exact sizes and
    # positions of the dock panes. This attribute is set by the framework.
    toolkit_state = Any
