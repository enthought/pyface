# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


""" The PyQt specific implementation of a menu bar manager. """


import sys

from traits.api import provides

from pyface.qt import QtGui
from pyface.action.action_manager import ActionManager
from pyface.action.i_menu_bar_manager import IMenuBarManager


@provides(IMenuBarManager)
class MenuBarManager(ActionManager):
    """ A menu bar manager realizes itself in errr, a menu bar control. """

    # ------------------------------------------------------------------------
    # 'MenuBarManager' interface.
    # ------------------------------------------------------------------------

    def create_menu_bar(self, parent, controller=None):
        """ Creates a menu bar representation of the manager. """

        # If a controller is required it can either be set as a trait on the
        # menu bar manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        # Create the menu bar. Work around disappearing menu bars on OS X
        # (particulary on PySide but also under certain circumstances on PyQt4).
        if isinstance(parent, QtGui.QMainWindow) and sys.platform == "darwin":
            parent.menuBar().setParent(None)
            menu_bar = parent.menuBar()
        else:
            menu_bar = QtGui.QMenuBar(parent)

        # Every item in every group must be a menu manager.
        for group in self.groups:
            for item in group.items:
                menu = item.create_menu(parent, controller)
                menu.menuAction().setText(item.name)
                menu_bar.addMenu(menu)

        return menu_bar
