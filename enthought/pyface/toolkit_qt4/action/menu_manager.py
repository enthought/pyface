#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtCore, QtGui


class MenuManager_qt4(object):
    """ The MenuManager monkey patch for Qt4. """

    ###########################################################################
    # 'MenuManager' toolkit interface.
    ###########################################################################

    def _tk_menumanager_create_menu(self, parent, controller):
        """ Create a menu with the given parent. """

        return _Menu(self, parent, controller)

    def _tk_menumanager_add_submenu(self, menu, submenu):
        """ Add a submenu to an existing menu. """

        submenu.menuAction().setText(self.name)
        menu.addMenu(submenu)

    def _tk_menumanager_add_separator(self, menu):
        """ Add a separator to a menu. """

        menu.addSeparator()


class _Menu(QtGui.QMenu):
    """ The toolkit-specific menu control. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, manager, parent, controller):
        """ Creates a new tree. """

        # Base class constructor.
        QtGui.QMenu.__init__(self, parent)

        # The parent of the menu.
        self._parent = parent
        
        # The manager that the menu is a view of.
        self._manager = manager

        # The controller.
        self._controller = controller

    ###########################################################################
    # '_Menu' interface.
    ###########################################################################

    def is_empty(self):
        """ Is the menu empty? """

        return self.isEmpty()

    def refresh(self):
        """ Ensures that the menu reflects the state of the manager. """

        self._manager._refresh_menu(self, self._parent, self._controller)

    def show(self, x, y):
        """ Show the menu at the specified location. """

        self.popup(QtCore.QPoint(x, y))
