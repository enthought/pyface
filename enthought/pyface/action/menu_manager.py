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
""" A menu manager realizes itself in a menu control. """


# Enthought library imports.
from enthought.traits.api import Str

# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from action_manager import ActionManager
from action_manager_item import ActionManagerItem
from group import Group


class MenuManager(ActionManager, ActionManagerItem):
    """ A menu manager realizes itself in a menu control.

    This could be a sub-menu or a context (popup) menu.
    """

    __tko__ = 'MenuManager'

    #### 'MenuManager' interface ##############################################
    
    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Str

    ###########################################################################
    # 'MenuManager' interface.
    ###########################################################################

    def create_menu(self, parent, controller=None):
        """ Creates a menu representation of the manager. """

        # ActionManager.__init__() would be the normal place to make sure the
        # toolkit was patched in for this class hierarchy.  The problem is that
        # TraitsUI creates a module level (ie. on import) menu bar which is too
        # soon to do the toolkit selection.  Instead each concrete
        # ActionManager sub-class must do the patching itself and not in its
        # __init__() method.
        patch_toolkit(self)

        # If a controller is required it can either be set as a trait on the
        # menu manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        menu = self._tk_menumanager_create_menu(parent, controller)

        # Create the menu structure.
        menu.refresh()

        # Listen to the manager being updated.
        self.on_trait_change(menu.refresh, 'changed')

        return menu

    ###########################################################################
    # 'ActionManagerItem' interface.
    ###########################################################################

    def add_to_menu(self, parent, menu, controller):
        """ Adds the item to a menu. """

        self._tk_menumanager_add_submenu(menu, self.create_menu(parent, controller))

        return

    def add_to_toolbar(self, parent, tool_bar, image_cache, controller):
        """ Adds the item to a tool bar. """

        raise ValueError("Cannot add a menu manager to a toolbar.")

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _refresh_menu(self, menu, parent, controller):
        """ Do the heavy lifting of populating a menu for the toolkit. """

        menu.clear()

        prev = None
        for group in self.groups:
            prev = self._add_group(menu, parent, controller, group, prev)

    def _add_group(self, menu, parent, controller, group, prev):
        """ Adds a group to a menu. """

        if len(group.items) > 0:
            # Is a separator required?
            if prev is not None and group.separator:
                self._tk_menumanager_add_separator(menu)

            # Create actions and sub-menus for each contribution item in the
            # group.
            for item in group.items:
                if isinstance(item, Group):
                    if len(item.items) > 0:
                        self._add_group(menu, parent, controller, item, prev)

                        if prev is not None and prev.separator and item.separator:
                            self._tk_menumanager_add_separator(menu)

                        prev = item

                else:
                    item.add_to_menu(parent, menu, controller)

            prev = group

        return prev

    ###########################################################################
    # 'MenuManager' toolkit interface.
    ###########################################################################

    def _tk_menumanager_create_menu(self, parent, controller):
        """ Create a menu with the given parent.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_menumanager_add_submenu(self, menu, submenu):
        """ Add a submenu to an existing menu.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_menumanager_add_separator(self, menu):
        """ Add a separator to a menu.
        
        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
