#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: David C. Morrill <dmorrill@enthought.com>
#
#-----------------------------------------------------------------------------
""" The base class for user perspective actions. """


# Enthought library imports.
from enthought.traits.api import on_trait_change

# Local imports.
from workbench_action import WorkbenchAction


class UserPerspectiveAction(WorkbenchAction):
    """ The base class for user perspective actions.

    Instances of this class (or its subclasses ;^) are enabled only when the
    active perspective is a user perspective.

    """
    
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

    @on_trait_change('window.active_perspective')
    def _refresh_enabled(self):
        """ Dynamic trait change handler. """

        self.enabled = self.window is not None \
          and self.window.active_perspective is not None \
          and self._is_user_perspective(self.window.active_perspective)
        
        return

    #### Methods ##############################################################
    
    def _is_user_perspective(self, perspective):
        """ Is the specified perspective a user perspective? """

        # fixme: This seems a bit of a smelly way to make the determinaction!
        id = perspective.id

        return ((id[:19] == '__user_perspective_') and (id[-2:] == '__'))

#### EOF #####################################################################
