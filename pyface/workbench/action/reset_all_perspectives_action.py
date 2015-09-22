""" An action that resets *all* perspectives. """


# Enthought library imports.
from pyface.api import YES

# Local imports.
from .workbench_action import WorkbenchAction


# The message used when confirming the action.
MESSAGE = 'Do you want to reset ALL perspectives to their defaults?'


class ResetAllPerspectivesAction(WorkbenchAction):
    """ An action that resets *all* perspectives. """

    #### 'Action' interface ###################################################

    # The action's unique identifier (may be None).
    id = 'pyface.workbench.action.reset_all_perspectives'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Reset All Perspectives'

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        window = self.window

        if window.confirm(MESSAGE) == YES:
            window.reset_all_perspectives()

        return

#### EOF ######################################################################
