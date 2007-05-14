""" A view containing a red panel! """


# Local imports.
from color_view import ColorView


class RedView(ColorView):
    """ A view containing a red panel! """

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Red'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'right'

#### EOF ######################################################################
