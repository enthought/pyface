# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, Str

from pyface.action.action import Action
from pyface.action.i_action_manager import IActionManager


class IMenuManager(IActionManager):
    """ A menu manager realizes itself in a menu control.

    This could be a sub-menu or a context (popup) menu.
    """

    # 'IMenuManager' interface ---------------------------------------------#

    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Str()

    # The default action for tool button when shown in a toolbar (Qt only)
    action = Instance(Action)

    # ------------------------------------------------------------------------
    # 'IMenuManager' interface.
    # ------------------------------------------------------------------------

    def create_menu(self, parent, controller=None):
        """ Creates a menu representation of the manager.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control that owns the menu.
        controller : pyface.action.action_controller.ActionController
            An optional ActionController for all items in the menu.
        """
