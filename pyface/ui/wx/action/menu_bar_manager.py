# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" The wx specific implementation of a menu bar manager.
"""


import wx

from traits.api import provides

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

        menu_bar = wx.MenuBar()

        # Every item in every group must be a menu manager.
        for group in self.groups:
            for item in group.items:
                menu = item.create_menu(parent, controller)
                menu_bar.Append(menu, item.name)

        return menu_bar
