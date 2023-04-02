# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that renames a user perspective. """


from .user_perspective_action import UserPerspectiveAction
from .user_perspective_name import UserPerspectiveName


class RenameUserPerspectiveAction(UserPerspectiveAction):
    """ An action that renames a user perspective. """

    # 'Action' interface ---------------------------------------------------

    # The action's unique identifier (may be None).
    id = "pyface.workbench.action.rename_user_perspective_action"

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Rename Perspective..."

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Perform the action. """

        window = event.window
        manager = window.workbench.user_perspective_manager

        # Get the new name.
        upn = UserPerspectiveName(name=window.active_perspective.name)
        if upn.edit_traits(view="rename_view").result:
            manager.rename(window.active_perspective, upn.name.strip())

        return
