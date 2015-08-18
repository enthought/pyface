#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: David C. Morrill <dmorrill@enthought.com>
#
#-----------------------------------------------------------------------------
""" An action that deletes a user perspective. """


# Enthought library imports.
from pyface.api import YES

# Local imports.
from .user_perspective_action import UserPerspectiveAction


class DeleteUserPerspectiveAction(UserPerspectiveAction):
    """ An action that deletes a user perspective. """

    #### 'Action' interface ###################################################

    # The action's unique identifier (may be None).
    id = 'pyface.workbench.action.delete_user_perspective_action'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Delete Perspective'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        window  = event.window
        manager = window.workbench.user_perspective_manager

        # The perspective to delete.
        perspective = window.active_perspective

        # Make sure that the user isn't having second thoughts!
        message = 'Are you sure you want to delete the "%s" perspective?' % \
                  perspective.name

        answer = window.confirm(message, title='Confirm Delete')
        if answer == YES:
            # Set the active perspective to be the first remaining perspective.
            #
            # There is always a default NON-user perspective (even if no
            # perspectives are explicitly defined) so we should never(!) not
            # be able to find one!
            window.active_perspective = self._get_next_perspective(window)

            # Remove the perspective from the window.
            window.perspectives.remove(perspective)

            # Remove it from the user perspective manager.
            manager.remove(perspective.id)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_next_perspective(self, window):
        """ Return the first perspective that is not the active one! """

        if window.active_perspective is window.perspectives[0]:
            index = 1

        else:
            index = 0

        return window.perspectives[index]

#### EOF #####################################################################
