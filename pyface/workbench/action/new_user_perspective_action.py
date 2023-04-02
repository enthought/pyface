# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that creates a new (and empty) user perspective. """


from .user_perspective_name import UserPerspectiveName
from .workbench_action import WorkbenchAction


class NewUserPerspectiveAction(WorkbenchAction):
    """ An action that creates a new (and empty) user perspective. """

    # 'Action' interface ---------------------------------------------------

    # The action's unique identifier.
    id = "pyface.workbench.action.new_user_perspective_action"

    # The action's name.
    name = "New Perspective..."

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Peform the action. """

        window = event.window
        manager = window.workbench.user_perspective_manager

        # Get the details of the new perspective.
        upn = UserPerspectiveName(name="User Perspective %d" % manager.next_id)
        if upn.edit_traits(view="new_view").result:
            # Create a new (and empty) user perspective.
            perspective = manager.create_perspective(
                upn.name.strip(), upn.show_editor_area
            )

            # Add it to the window...
            window.perspectives.append(perspective)

            # ... and make it the active perspective.
            window.active_perspective = perspective

        return
