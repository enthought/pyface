#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class MenuBarManager_qt4(object):
    """ The MenuBarManager monkey patch for Qt4. """

    ###########################################################################
    # 'MenuManager' toolkit interface.
    ###########################################################################

    def _tk_menubarmanager_create_menu_bar(self, parent):
        """ Create a menu bar with the given parent. """

        return QtGui.QMenuBar(parent)

    def _tk_menubarmanager_add_menu(self, menu_bar, menu, name):
        """ Add a menu to a menu bar. """

        menu.menuAction().setText(name)
        menu_bar.addMenu(menu)
