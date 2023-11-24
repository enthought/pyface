# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" The interface for a menu bar manager. """

from pyface.action.i_action_manager import IActionManager


class IMenuBarManager(IActionManager):
    """ The interface for a menu bar manager. """

    # ------------------------------------------------------------------------
    # 'MenuBarManager' interface.
    # ------------------------------------------------------------------------

    def create_menu_bar(self, parent, controller=None):
        """ Creates a menu bar representation of the manager.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control that owns the menubar.
        controller : pyface.action.action_controller.ActionController
            An optional ActionController for all items in the menubar.
        """
