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

# Major package imports.
import wx


class MenuManager_wx(object):
    """ The MenuManager monkey patch for wx. """

    ###########################################################################
    # 'MenuManager' toolkit interface.
    ###########################################################################

    def _tk_menumanager_create_menu(self, parent, controller):
        """ Create a menu with the given parent. """

        return _Menu(self, parent, controller)

    def _tk_menumanager_add_submenu(self, menu, submenu):
        """ Add a submenu to an existing menu. """

        menu.AppendMenu(wx.NewId(), self.name, submenu)

        return

    def _tk_menumanager_add_separator(self, menu):
        """ Add a separator to a menu. """

        menu.AppendSeparator()

        return


class _Menu(wx.Menu):
    """ The toolkit-specific menu control. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, manager, parent, controller):
        """ Creates a new tree. """

        # Base class constructor.
        wx.Menu.__init__(self)

        # The parent of the menu.
        self._parent = parent
        
        # The manager that the menu is a view of.
        self._manager = manager

        # The controller.
        self._controller = controller

        return

    ###########################################################################
    # '_Menu' interface.
    ###########################################################################

    def clear(self):
        """ Clears the items from the menu. """
        
        for item in self.GetMenuItems():
            self.Delete(item.GetId())

        return

    def is_empty(self):
        """ Is the menu empty? """

        return self.GetMenuItemCount() == 0

    def refresh(self):
        """ Ensures that the menu reflects the state of the manager. """

        self._manager._refresh_menu(self, self._parent, self._controller)

        return

    def show(self, x, y):
        """ Show the menu at the specified location. """

        self._parent.PopupMenuXY(self, x, y)

        return

#### EOF ######################################################################
