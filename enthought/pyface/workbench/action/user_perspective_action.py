#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: David C. Morrill <dmorrill@enthought.com>
#
#-----------------------------------------------------------------------------
""" The base class for user perspective actions. """


# Local imports.
from workbench_action import WorkbenchAction


class UserPerspectiveAction(WorkbenchAction):
    """ The base class for user perspective actions.

    Instances of this class (or its subclasses ;^) are enabled only when the
    active perspective is a user perspective.

    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Constructor. """

        super(UserPerspectiveAction, self).__init__(**traits)

        # Make sure that the action is enabled if the active perspective is a
        # user perspective.
        self._refresh_enabled()

        return
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the action. """

        # This removes the active perspective listener.
        self.window = None

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait change handlers ################################################

    def _window_changed(self, old, new):
        """ Static trait change handler. """

        if old is not None:
            old.on_trait_change(
                self._refresh_enabled, 'active_perspective', remove=True
            )

        if new is not None:
            new.on_trait_change(
                self._refresh_enabled, 'active_perspective'
            )

        return

    #### Methods ##############################################################
    
    def _is_user_perspective(self, perspective):
        """ Is the specified perspective a user perspective? """

        # fixme: This seems a bit of a smelly way to make the determinaction!
        id = perspective.id

        return ((id[:19] == '__user_perspective_') and (id[-2:] == '__'))

    def _refresh_enabled(self):
        """ Refresh the enabled state of the action. """

        self.enabled = self.window is not None \
         and self._is_user_perspective(self.window.active_perspective)
        
        return
    

#### EOF #####################################################################
