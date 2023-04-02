# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The 'null' backend specific implementation of the tool bar manager.
"""


from traits.api import Bool, Enum, Instance, Tuple


from pyface.image_cache import ImageCache
from pyface.action.action_manager import ActionManager


class ToolBarManager(ActionManager):
    """ A tool bar manager realizes itself in errr, a tool bar control. """

    # 'ToolBarManager' interface -------------------------------------------

    # The size of tool images (width, height).
    image_size = Tuple((16, 16))

    # The orientation of the toolbar.
    orientation = Enum("horizontal", "vertical")

    # Should we display the name of each tool bar tool under its image?
    show_tool_names = Bool(True)

    # Should we display the horizontal divider?
    show_divider = Bool(True)

    # Private interface ----------------------------------------------------

    # Cache of tool images (scaled to the appropriate size).
    _image_cache = Instance(ImageCache)

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, *args, **traits):
        """ Creates a new tool bar manager. """

        # Base class contructor.
        super().__init__(*args, **traits)

        # An image cache to make sure that we only load each image used in the
        # tool bar exactly once.
        self._image_cache = ImageCache(self.image_size[0], self.image_size[1])

        return

    # ------------------------------------------------------------------------
    # 'ToolBarManager' interface.
    # ------------------------------------------------------------------------

    def create_tool_bar(self, parent, controller=None):
        """ Creates a tool bar. """

        # If a controller is required it can either be set as a trait on the
        # tool bar manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        return None
