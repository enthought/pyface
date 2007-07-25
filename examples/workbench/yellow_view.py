""" A view containing a yellow panel! """


# Local imports.
from color_view import ColorView


class YellowView(ColorView):
    """ A view containing a yellow panel! """

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Yellow'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'with'

    # The Id of the view to position this view relative to. If this is not
    # specified (or if no view exists with this Id) then the view will be
    # placed relative to the editor area.
    relative_to = 'Green'

#### EOF ######################################################################
