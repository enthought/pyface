# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging

from .checkbox_image_renderer import CheckboxImageRenderer
from .grid_cell_renderer import GridCellRenderer


logger = logging.getLogger(__name__)


class CheckboxRenderer(GridCellRenderer):
    def __init__(self, **traits):

        # base-class constructor
        super().__init__(**traits)

        # initialize the renderer, if it hasn't already been initialized
        if self.renderer is None:
            self.renderer = CheckboxImageRenderer()

    def on_left_click(self, grid, row, col):
        """ Toggles the value. """

        value = grid.model.get_cell_drag_value(row, col)

        try:
            grid.model.set_value(row, col, not value)
        except Exception:
            logger.exception("Can't set cell value")

        return True
