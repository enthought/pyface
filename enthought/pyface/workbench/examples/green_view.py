""" A view containing a green panel! """


# Local imports.
from color_view import ColorView


class GreenView(ColorView):
    """ A view containing a green panel! """

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Green'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'left'

#### EOF ######################################################################
