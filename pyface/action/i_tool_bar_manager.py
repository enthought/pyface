# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Bool, Str, Tuple

from pyface.action.i_action_manager import IActionManager
from pyface.ui_traits import Orientation


class IToolBarManager(IActionManager):
    """ The interface for a tool bar manager. """

    # 'IToolBarManager' interface -------------------------------------------

    # The size of tool images (width, height).
    image_size = Tuple((16, 16))

    # The toolbar name (used to distinguish multiple toolbars).
    name = Str("ToolBar")

    # The orientation of the toolbar.
    orientation = Orientation("horizontal")

    # Should we display the name of each tool bar tool under its image?
    show_tool_names = Bool(True)

    # Should we display the horizontal divider?
    show_divider = Bool(True)

    # ------------------------------------------------------------------------
    # 'ToolBarManager' interface.
    # ------------------------------------------------------------------------

    def create_tool_bar(self, parent, controller=None):
        """ Creates a tool bar.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control that owns the toolbar.
        controller : pyface.action.action_controller.ActionController
            An optional ActionController for all items in the toolbar.
        """
