#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: David C. Morrill <dmorrill@enthought.com>
#
#-----------------------------------------------------------------------------
""" An action that creates a new (and empty) user perspective. """


# Local imports.
from .user_perspective_name import UserPerspectiveName
from .workbench_action import WorkbenchAction


class NewUserPerspectiveAction(WorkbenchAction):
    """ An action that creates a new (and empty) user perspective. """

    #### 'Action' interface ###################################################

    # The action's unique identifier.
    id = 'pyface.workbench.action.new_user_perspective_action'

    # The action's name.
    name = 'New Perspective...'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Peform the action. """

        window  = event.window
        manager = window.workbench.user_perspective_manager

        # Get the details of the new perspective.
        upn = UserPerspectiveName(name='User Perspective %d' % manager.next_id)
        if upn.edit_traits(view='new_view').result:
            # Create a new (and empty) user perspective.
            perspective = manager.create_perspective(
                upn.name.strip(), upn.show_editor_area
            )

            # Add it to the window...
            window.perspectives.append(perspective)

            # ... and make it the active perspective.
            window.active_perspective = perspective

        return

#### EOF #####################################################################
