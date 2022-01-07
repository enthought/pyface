# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import logging

logger = logging.getLogger(__name__)
logger.warning("DEPRECATED: pyface.grid, use pyface.ui.wx.grid instead.")

from pyface.ui.wx.grid.composite_grid_model import *  # noqa: F401
