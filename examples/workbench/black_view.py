""" A view containing a black panel! """


# Local imports.
from color_view import ColorView


class BlackView(ColorView):
    """ A view containing a black panel! """

    #### 'IView' interface ####################################################

    # The view's name.
    name = 'Black'

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = 'top'

#### EOF ######################################################################
