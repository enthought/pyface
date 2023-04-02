# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The menu bar manager for Envisage workbench windows. """


from pyface.action.api import MenuBarManager as BaseMenuBarManager
from traits.api import Instance


from .action_controller import ActionController


class MenuBarManager(BaseMenuBarManager):
    """ The menu bar manager for Envisage workbench windows. """

    # 'MenuBarManager' interface -------------------------------------------

    # The workbench window that we are the menu bar manager for.
    window = Instance("pyface.workbench.api.WorkbenchWindow")

    # ------------------------------------------------------------------------
    # 'MenuBarManager' interface.
    # ------------------------------------------------------------------------

    def create_menu_bar(self, parent):
        """ Creates a menu bar representation of the manager. """

        # The controller handles the invocation of every action.
        controller = ActionController(window=self.window)

        menu_bar = super().create_menu_bar(parent, controller=controller)

        return menu_bar
