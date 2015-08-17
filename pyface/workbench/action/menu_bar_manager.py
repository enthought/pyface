""" The menu bar manager for Envisage workbench windows. """


# Enthought library imports.
from pyface.action.api import MenuBarManager as BaseMenuBarManager
from traits.api import Instance

# Local imports.
from .action_controller import ActionController


class MenuBarManager(BaseMenuBarManager):
    """ The menu bar manager for Envisage workbench windows. """

    #### 'MenuBarManager' interface ###########################################

    # The workbench window that we are the menu bar manager for.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'MenuBarManager' interface.
    ###########################################################################

    def create_menu_bar(self, parent):
        """ Creates a menu bar representation of the manager. """

        # The controller handles the invocation of every action.
        controller = ActionController(window=self.window)

        menu_bar = super(MenuBarManager, self).create_menu_bar(
            parent, controller=controller
        )

        return menu_bar

#### EOF ######################################################################
