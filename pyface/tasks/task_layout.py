# Enthought library imports.
from traits.api import Any, Either, Enum, HasStrictTraits, List, Str

# Trait definitions.
NestedListStr = List(Either(Str, List(Str)))


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

    # Assignments of dock areas to the window's corners. By default, the top and
    # bottom dock areas extend into both of the top and both of the bottom
    # corners, respectively.
    top_left_corner = Enum('top', 'left')
    top_right_corner = Enum('top', 'right')
    bottom_left_corner = Enum('bottom', 'left')
    bottom_right_corner = Enum('bottom', 'right')

    # A toolkit-specific state object which encodes the exact sizes and
    # positions of the dock panes. This attribute is set by the framework.
    toolkit_state = Any
