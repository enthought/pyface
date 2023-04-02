# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The base class for user perspective actions. """


from traits.api import observe


from .workbench_action import WorkbenchAction


class UserPerspectiveAction(WorkbenchAction):
    """ The base class for user perspective actions.

    Instances of this class (or its subclasses ;^) are enabled only when the
    active perspective is a user perspective.

    """

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def destroy(self):
        """ Destroy the action. """

        # This removes the active perspective listener.
        self.window = None

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _is_user_perspective(self, perspective):
        """ Is the specified perspective a user perspective? """

        # fixme: This seems a bit of a smelly way to make the determinaction!
        id = perspective.id

        return (id[:19] == "__user_perspective_") and (id[-2:] == "__")

    @observe("window.active_perspective")
    def _refresh_enabled(self, event):
        """ Refresh the enabled state of the action. """

        self.enabled = (
            self.window is not None
            and self.window.active_perspective is not None
            and self._is_user_perspective(self.window.active_perspective)
        )

        return
