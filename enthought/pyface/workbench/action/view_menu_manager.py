""" A simple(istic!) menu manager for all of the views in a window. """


# Enthought library imports.
from enthought.pyface.action.api import Group, MenuManager
from enthought.traits.api import Any, Bool, Instance, List, Str, Unicode
from enthought.traits.api import on_trait_change

# Local imports.
from perspective_menu_manager import PerspectiveMenuManager
from toggle_view_visibility_action import ToggleViewVisibilityAction


# Logging.
import logging; logger = logging.getLogger()


class ViewMenuManager(MenuManager):
    """ A simple(istic!) menu manager for all of the views in a window.

    Every possible view in the window gets its own menu entry. Obviously this
    does not scale!

    """

    #### 'ActionManager' interface ############################################

    # All of the groups in the manager.
    groups = List(Group)

    # The manager's unique identifier (if it has one).
    id = Str('View')

    #### 'MenuManager' interface ##############################################

    # The menu manager's name (if the manager is a sub-menu, this is what its
    # label will be).
    name = Unicode('&View')

    #### 'ViewMenuManager' interface ##########################################

    # Should the (also non-scaleable!) perspective menu be shown?
    show_perspective_menu = Bool(True)
    
    # The workbench window that the menu is part of.
    window = Instance('enthought.pyface.workbench.api.WorkbenchWindow')

    #### 'Private' interface ##################################################

    # The group containing the view hide/show actions.
    _view_group = Any
    
    ###########################################################################
    # 'ActionManager' interface.
    ###########################################################################

    def _groups_default(self):
        """ Trait initializer. """

        groups = []
        
        # Add a group containing the perspective menu (if requested).
        if self.show_perspective_menu and len(self.window.perspectives) > 0:
            groups.append(Group(PerspectiveMenuManager(window=self.window)))
            
        # Add a group containing a 'toggler' for each view.
        self._view_group = self._create_view_group(self.window)
        groups.append(self._view_group)

        return groups
    
    ###########################################################################
    # 'ViewMenuManager' interface.
    ###########################################################################

    def refresh(self):
        """ Refreshes the checked state of the actions in the menu. """

        logger.debug('refreshing view menu')

        if self._view_group is not None:
            for view in self.window.views:
                action_item = self._view_group.find(view.id)
                action_item.action.checked = view.visible

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_view_group(self, window):
        """ Creates a group containing the view 'togglers'. """

        group = Group()
        for view in window.views:
            group.append(ToggleViewVisibilityAction(view=view, window=window))

        return group

    #### Trait change handlers ################################################

    @on_trait_change('window.active_perspective')
    def when_window_active_perspective_changed(self, new):
        """ Static trait change handler. """

        self.refresh()

        return

#### EOF ######################################################################
