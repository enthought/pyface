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
""" A menu bar manager realizes itself in errr, a menu bar control. """


# Private Enthought library imports.
from enthought.pyface.toolkit import patch_toolkit

# Local imports.
from action_manager import ActionManager


class MenuBarManager(ActionManager):
    """ A menu bar manager realizes itself in errr, a menu bar control. """

    __tko__ = 'MenuBarManager'

    ###########################################################################
    # 'MenuManager' interface.
    ###########################################################################

    def create_menu_bar(self, parent, controller=None):
        """ Creates a menu bar representation of the manager. """

        # ActionManager.__init__() would be the normal place to make sure the
        # toolkit was patched in for this class hierarchy.  The problem is that
        # TraitsUI creates a module level (ie. on import) menu bar which is too
        # soon to do the toolkit selection.  Instead each concrete
        # ActionManager sub-class must do the patching itself and not in its
        # __init__() method.
        patch_toolkit(self)

        # If a controller is required it can either be set as a trait on the
        # menu bar manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller
            
        menu_bar = self._tk_menubarmanager_create_menu_bar(parent)
        
        # Every item in every group must be a menu manager.
        for group in self.groups:
            for item in group.items:
                menu = item.create_menu(parent, controller)
                self._tk_menubarmanager_add_menu(menu_bar, menu, item.name)
                 
        return menu_bar

    ###########################################################################
    # 'MenuManager' toolkit interface.
    ###########################################################################

    def _tk_menubarmanager_create_menu_bar(self, parent):
        """ Create a menu bar with the given parent.
        
        This must be reimplemented.
        """

        raise NotImplementedError

    def _tk_menubarmanager_add_menu(self, menu_bar, menu, name):
        """ Add a menu to a menu bar.
        
        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
