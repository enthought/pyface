""" A view containing a blue panel! """


from color_view import ColorView


class BlueView(ColorView):
    """ A view containing a blue panel! """

    # 'IView' interface ----------------------------------------------------

    # The view's name.
    name = "Blue"

    # The default position of the view relative to the item specified in the
    # 'relative_to' trait.
    position = "bottom"
