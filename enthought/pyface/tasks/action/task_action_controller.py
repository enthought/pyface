# Enthought library imports.
from enthought.pyface.action.api import ActionController
from enthought.traits.api import Instance

# Local imports.
from enthought.pyface.tasks.task import Task


class TaskActionController(ActionController):
    """ An action controller for menu and tool bars.

    The controller is used to 'hook' the invocation of every action on the menu
    and tool bars. This is done so that additional, Task-specific information
    can be added to action events. Currently, we attach a reference to the Task.
    """

    #### TaskActionController interface #######################################

    # The task that this is the controller for.
    task = Instance(Task)

    ###########################################################################
    # 'ActionController' interface.
    ###########################################################################

    def perform(self, action, event):
        """ Control an action invocation.
        """
        event.task = self.task
        return action.perform(event)
