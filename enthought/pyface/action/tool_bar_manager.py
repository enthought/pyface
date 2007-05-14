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
""" A tool bar manager realizes itself in errr, a tool bar control. """


# Enthought library imports.
from enthought.pyface.image_cache import ImageCache
from enthought.traits.api import Any, Bool, Enum, Instance, Tuple

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from action_manager import ActionManager


class ToolBarManager(ActionManager):
    """ A tool bar manager realizes itself in errr, a tool bar control. """

    __tko__ = 'ToolBarManager'

    #### 'ToolBarManager' interface ###########################################
    
    # The size of tool images (width, height).
    image_size = Tuple((16, 16))

    # The orientation of the toolbar.
    orientation = Enum('horizontal', 'vertical')

    # Should we display the name of each tool bar tool under its image?
    show_tool_names = Bool(True)
    
    # Should we display the horizontal divider?
    show_divider = Bool(True)

    #### Private interface ####################################################

    # Cache of tool images (scaled to the appropriate size).
    _image_cache = Instance(ImageCache)

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **traits):
        """ Creates a new tool bar manager. """

        # Base class contructor.
        super(ToolBarManager, self).__init__(*args, **traits)

        # An image cache to make sure that we only load each image used in the
        # tool bar exactly once.
        self._image_cache = ImageCache(self.image_size[0], self.image_size[1])
        
        return

    ###########################################################################
    # 'ToolBarManager' interface.
    ###########################################################################

    def create_tool_bar(self, parent, controller=None):
        """ Creates a tool bar. """

        # ActionManager.__init__() would be the normal place to make sure the
        # toolkit was patched in for this class hierarchy.  The problem is that
        # TraitsUI creates a module level (ie. on import) menu bar which is too
        # soon to do the toolkit selection.  Instead each concrete
        # ActionManager sub-class must do the patching itself and not in its
        # __init__() method.
        patch_toolkit(self)

        # If a controller is required it can either be set as a trait on the
        # tool bar manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        # Create the tool bar.
        tool_bar = self._tk_toolbarmanager_create_tool_bar(parent)

        # Add all of items in the manager's groups to the tool bar.
        self._add_tools(parent, tool_bar, controller)
        
        # This is only to allow wx to do some workarounds.
        self._tk_toolbarmanager_fixup(tool_bar)

        return tool_bar

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_tools(self, parent, tool_bar, controller):
        """ Adds tools for all items in the list of groups. """
        
        previous_non_empty_group = None
        for group in self.groups:
            if len(group.items) > 0:
                # Is a separator required?
                if previous_non_empty_group is not None and group.separator:
                    self._tk_toolbarmanager_add_separator(tool_bar)

                previous_non_empty_group = group

                # Create a tool bar tool for each item in the group.
                for item in group.items:
                    item.add_to_toolbar(
                        parent,
                        tool_bar,
                        self._image_cache,
                        controller,
                        self.show_tool_names
                    )

        return

    ###########################################################################
    # 'ToolBarManager' toolkit interface.
    ###########################################################################

    def _tk_toolbarmanager_create_tool_bar(self, parent):
        """ Create a tool bar with the given parent.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_toolbarmanager_add_separator(self, tool_bar):
        """ Add a separator to a toolbar.

        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_toolbarmanager_fixup(self, tool_bar):
        """ Handle any required fixups after the tool bar has been created. """

        pass

#### EOF ######################################################################
