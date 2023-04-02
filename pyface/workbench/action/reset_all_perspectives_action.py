# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that resets *all* perspectives. """


from pyface.api import YES


from .workbench_action import WorkbenchAction


# The message used when confirming the action.
MESSAGE = "Do you want to reset ALL perspectives to their defaults?"


class ResetAllPerspectivesAction(WorkbenchAction):
    """ An action that resets *all* perspectives. """

    # 'Action' interface ---------------------------------------------------

    # The action's unique identifier (may be None).
    id = "pyface.workbench.action.reset_all_perspectives"

    # The action's name (displayed on menus/tool bar tools etc).
    name = "Reset All Perspectives"

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Perform the action. """

        window = self.window

        if window.confirm(MESSAGE) == YES:
            window.reset_all_perspectives()

        return
