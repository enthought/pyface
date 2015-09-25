""" The default action controller for menus, menu bars and tool bars. """


# Enthought library imports.
from traits.api import HasTraits


class ActionController(HasTraits):
    """ The default action controller for menus, menu bars and tool bars. """

    ###########################################################################
    # 'ActionController' interface.
    ###########################################################################

    def perform(self, action, event):
        """ Control an action invocation.

        Parameters
        ----------
        action : Action instance
            The action to perform.
        event : ActionEvent instance
            The event that triggered the action.

        Returns
        -------
        result : any
            The result of the action's perform method (usually None).
        """
        return action.perform(event)

    def can_add_to_menu(self, action):
        """ Can add an action to a menu

        Parameters
        ----------
        action : Action instance
            The action to consider.

        Returns
        -------
        can_add : bool
            ``True` if the action can be added to a menu/menubar.
        """
        return True

    def add_to_menu(self, action):
        """ Called when an action is added to the a menu/menubar.

        Parameters
        ----------
        action : Action instance
            The action added to the menu.
        """
        pass

    def can_add_to_toolbar(self, action):
        """ Returns True if the action can be added to a toolbar.

        Parameters
        ----------
        action : Action instance
            The action to consider.

        Returns
        -------
        can_add : bool
            ``True` if the action can be added to a toolbar.
        """
        return True

    def add_to_toolbar(self, action):
        """ Called when an action is added to the a toolbar.

        Parameters
        ----------
        action : Action instance
            The action added to the toolbar.
        """
        pass
