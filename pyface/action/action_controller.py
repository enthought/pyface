""" The default action controller for menus, menu bars and tool bars. """


# Enthought library imports.
from traits.api import HasTraits


class ActionController(HasTraits):
    """ The default action controller for menus, menu bars and tool bars. """

    ###########################################################################
    # 'ActionController' interface.
    ###########################################################################

    def perform(self, action, event):
        """ Control an action invocation. """

        return action.perform(event)

    def can_add_to_menu(self, action):
        """ Returns True if the action can be added to a menu/menubar. """

        return True

    def add_to_menu(self, action):
        """ Called when an action is added to the a menu/menubar. """

        return

    def can_add_to_toolbar(self, action):
        """ Returns True if the action can be added to a toolbar. """

        return True

    def add_to_toolbar(self, action):
        """ Called when an action is added to the a toolbar. """

        return

#### EOF ######################################################################
