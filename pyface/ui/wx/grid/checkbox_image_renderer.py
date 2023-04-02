# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A renderer which displays a checked-box for a True value and an unchecked
    box for a false value. """


from pyface.image_resource import ImageResource


from .mapped_grid_cell_image_renderer import MappedGridCellImageRenderer

checked_image_map = {
    True: ImageResource("checked"),
    False: ImageResource("unchecked"),
}


class CheckboxImageRenderer(MappedGridCellImageRenderer):
    def __init__(self, display_text=False):

        text_map = None
        if display_text:
            text_map = {True: "True", False: "False"}

        # Base-class constructor
        super().__init__(checked_image_map, text_map)

        return
