#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" A tool bar manager realizes itself in a tool palette control. """


# Enthought library imports.
from traits.api import Any, Bool, Enum, Instance, Tuple

# Local imports.
from pyface.image_cache import ImageCache
from pyface.action.action_manager import ActionManager
from .tool_palette import ToolPalette


class ToolPaletteManager(ActionManager):
    """ A tool bar manager realizes itself in a tool palette bar control. """

    #### 'ToolPaletteManager' interface #######################################

    # The size of tool images (width, height).
    image_size = Tuple((16, 16))

    # Should we display the name of each tool bar tool under its image?
    show_tool_names = Bool(True)

    #### Private interface ####################################################

    # Cache of tool images (scaled to the appropriate size).
    _image_cache = Instance(ImageCache)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Creates a new tool bar manager. """

        # Base class contructor.
        super(ToolPaletteManager, self).__init__(*args, **traits)

        # An image cache to make sure that we only load each image used in the
        # tool bar exactly once.
        self._image_cache = ImageCache(self.image_size[0], self.image_size[1])

        return

    ###########################################################################
    # 'ToolPaletteManager' interface.
    ###########################################################################

    def create_tool_palette(self, parent, controller=None):
        """ Creates a tool bar. """
        return None


#### EOF ######################################################################
