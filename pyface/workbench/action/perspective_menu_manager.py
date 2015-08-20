""" The default perspective menu for a workbench window. """


# Enthought library imports.
from pyface.action.api import Group, MenuManager
from traits.api import Instance, List, on_trait_change

# Local imports.
from .delete_user_perspective_action import DeleteUserPerspectiveAction
from .new_user_perspective_action import NewUserPerspectiveAction
from .rename_user_perspective_action import RenameUserPerspectiveAction
from .reset_all_perspectives_action import ResetAllPerspectivesAction
from .reset_active_perspective_action import ResetActivePerspectiveAction
from .save_as_user_perspective_action import SaveAsUserPerspectiveAction
from .set_active_perspective_action import SetActivePerspectiveAction


class PerspectiveMenuManager(MenuManager):
    """ The default perspective menu for a workbench window. """

    #### 'ActionManager' interface ############################################

    # All of the groups in the manager.
    groups = List(Group)

    # The manager's unique identifier.
    id = 'PerspectivesMenu'

    #### 'MenuManager' interface ##############################################

    # The menu manager's name.
    name = 'Perspectives'

    #### 'PerspectiveMenuManager' interface ###################################

    # The workbench window that the manager is part of.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    ###########################################################################
    # 'ActionManager' interface.
    ###########################################################################

    def _groups_default(self):
        """ Trait initializer. """

        groups = [
            # Create a group containing the actions that switch to specific
            # perspectives.
            self._create_perspective_group(self.window),

            # Create a group containing the user perspective create/save/rename
            # /delete actions.
            self._create_user_perspective_group(self.window),

            # Create a group containing the reset actions.
            self._create_reset_perspective_group(self.window)

        ]

        return groups

    ###########################################################################
    # 'PerspectiveMenuManager' interface.
    ###########################################################################

    @on_trait_change('window.perspectives')
    @on_trait_change('window.perspectives_items')
    def rebuild(self):
        """ Rebuild the menu.

        This is called when user perspectives have been added or removed.

        """

        # Clear out the old menu. This gives any actions that have trait
        # listeners (i.e. the rename and delete actions!) a chance to unhook
        # them.
        self.destroy()

        # Resetting the trait allows the initializer to run again (which will
        # happen just as soon as we fire the 'changed' event).
        self.reset_traits(['groups'])

        # Let the associated menu know that we have changed.
        self.changed = True

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_perspective_group(self, window):
        """ Create the actions that switch to specific perspectives. """

        # fixme: Not sure if alphabetic sorting is appropriate in all cases,
        # but it will do for now!
        perspectives = window.perspectives[:]
        perspectives.sort(key=lambda x:x.name)

        # For each perspective, create an action that sets the active
        # perspective to it.
        group = Group()
        for perspective in perspectives:
            group.append(
                SetActivePerspectiveAction(
                    perspective=perspective, window=window
                )
            )

        return group

    def _create_user_perspective_group(self, window):
        """ Create the user perspective create/save/rename/delete actions. """

        group = Group(
            NewUserPerspectiveAction(window=window),
            SaveAsUserPerspectiveAction(window=window),
            RenameUserPerspectiveAction(window=window),
            DeleteUserPerspectiveAction(window=window)
        )

        return group

    def _create_reset_perspective_group(self, window):
        """ Create the reset perspective actions. """

        group = Group(
            ResetActivePerspectiveAction(window=window),
            ResetAllPerspectivesAction(window=window)
        )

        return group

#### EOF ######################################################################
