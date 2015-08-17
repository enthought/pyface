""" An item in a Perspective contents list. """


# Enthought library imports.
from traits.api import Enum, Float, HasTraits, provides, Str

# Local imports.
from .i_perspective_item import IPerspectiveItem


@provides(IPerspectiveItem)
class PerspectiveItem(HasTraits):
    """ An item in a Perspective contents list. """
    # The Id of the view to display in the perspective.
    id = Str

    # The position of the view relative to the item specified in the
    # 'relative_to' trait.
    #
    # 'top'    puts the view above the 'relative_to' item.
    # 'bottom' puts the view below the 'relative_to' item.
    # 'left'   puts the view to the left of  the 'relative_to' item.
    # 'right'  puts the view to the right of the 'relative_to' item.
    # 'with'   puts the view in the same region as the 'relative_to' item.
    #
    # If the position is specified as 'with' you must specify a 'relative_to'
    # item other than the editor area (i.e., you cannot position a view 'with'
    # the editor area).
    position = Enum('left', 'top', 'bottom', 'right', 'with')

    # The Id of the view to position relative to. If this is not specified
    # (or if no view exists with this Id) then the view will be placed relative
    # to the editor area.
    relative_to = Str

    # The width of the item (as a fraction of the window width).
    #
    # e.g. 0.5 == half the window width.
    #
    # Note that this is treated as a suggestion, and it may not be possible
    # for the workbench to allocate the space requested.
    width = Float(-1)

    # The height of the item (as a fraction of the window height).
    #
    # e.g. 0.5 == half the window height.
    #
    # Note that this is treated as a suggestion, and it may not be possible
    # for the workbench to allocate the space requested.
    height = Float(-1)

    # The style of the dock control created.
    style_hint = Enum('tab', 'vertical', 'horizontal', 'fixed')

#### EOF ######################################################################
