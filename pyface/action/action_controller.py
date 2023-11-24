# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The default action controller for menus, menu bars and tool bars. """


from traits.api import HasTraits


class ActionController(HasTraits):
    """ The default action controller for menus, menu bars and tool bars. """

    # ------------------------------------------------------------------------
    # 'ActionController' interface.
    # ------------------------------------------------------------------------

    def perform(self, action, event):
        """ Control an action invocation.

        Parameters
        ----------
        action : Action
            The action to perform.
        event : ActionEvent
            The event that triggered the action.

        Returns
        -------
        result : Any
            The result of the action's perform method (usually None).
        """
        return action.perform(event)

    def can_add_to_menu(self, action):
        """ Can add an action to a menu

        Parameters
        ----------
        action : Action
            The action to consider.

        Returns
        -------
        can_add : bool
            ``True`` if the action can be added to a menu/menubar.
        """
        return True

    def add_to_menu(self, action):
        """ Called when an action is added to the a menu/menubar.

        Parameters
        ----------
        action : Action
            The action added to the menu.
        """
        pass

    def can_add_to_toolbar(self, action):
        """ Returns True if the action can be added to a toolbar.

        Parameters
        ----------
        action : Action
            The action to consider.

        Returns
        -------
        can_add : bool
            ``True`` if the action can be added to a toolbar.
        """
        return True

    def add_to_toolbar(self, action):
        """ Called when an action is added to the a toolbar.

        Parameters
        ----------
        action : Action
            The action added to the toolbar.
        """
        pass
