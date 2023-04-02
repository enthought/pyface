# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from .edit_image_renderer import EditImageRenderer
from .grid_cell_renderer import GridCellRenderer


class EditRenderer(GridCellRenderer):
    def __init__(self, **traits):

        # base-class constructor
        super().__init__(**traits)

        # initialize the renderer, if it hasn't already been initialized
        if self.renderer is None:
            self.renderer = EditImageRenderer()

    def on_left_click(self, grid, row, col):
        """ Calls edit_traits on the object represented by the row. """

        obj = grid.model.get_rows_drag_value([row])[0]

        # allow editting if the obj does not have an editable trait
        # or if the editable trait is True

        if (not hasattr(obj, "editable")) or obj.editable:
            obj.edit_traits(kind="live")
