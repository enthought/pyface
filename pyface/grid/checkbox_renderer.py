import logging

logger = logging.getLogger(__name__)
logger.warning('DEPRECATED: pyface.grid, use pyface.ui.wx.grid instead.')

from pyface.ui.wx.grid.checkbox_renderer import *
