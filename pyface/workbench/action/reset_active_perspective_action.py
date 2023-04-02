# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that resets the active perspective. """


from pyface.api import YES


from .workbench_action import WorkbenchAction


# The message used when confirming the action.
MESSAGE = 'Do you want to reset the current "%s" perspective to its defaults?'


class ResetActivePerspectiveAction(WorkbenchAction):
    """ An action that resets the active perspective. """

    # 'Action' interface ---------------------------------------------------

    # The action's unique identifier (may be None).
    id = "pyface.workbench.action.reset_active_perspective"

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Reset Perspective"

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Perform the action. """

        window = self.window

        if window.confirm(MESSAGE % window.active_perspective.name) == YES:
            window.reset_active_perspective()

        return
