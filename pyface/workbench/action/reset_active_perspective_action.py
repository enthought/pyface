""" An action that resets the active perspective. """


# Enthought library imports.
from pyface.api import YES

# Local imports.
from .workbench_action import WorkbenchAction


# The message used when confirming the action.
MESSAGE = 'Do you want to reset the current "%s" perspective to its defaults?'


class ResetActivePerspectiveAction(WorkbenchAction):
    """ An action that resets the active perspective. """

    #### 'Action' interface ###################################################

    # The action's unique identifier (may be None).
    id = 'pyface.workbench.action.reset_active_perspective'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Reset Perspective'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        window = self.window

        if window.confirm(MESSAGE % window.active_perspective.name) == YES:
            window.reset_active_perspective()

        return

#### EOF ######################################################################
