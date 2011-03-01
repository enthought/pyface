# Enthought library imports.
from enthought.pyface.tasks.api import Task, TaskPane
from enthought.traits.api import Bool, Instance, Property, cached_property

# Local imports.
from listening_action import ListeningAction


class TaskAction(ListeningAction):
    """ An Action that makes a callback to a Task.

    Note that this is a convenience class. Actions associated with a Task need
    not inherit TaskAction, although they must, of course, inherit Action.
    """

    #### ListeningAction interface ############################################

    object = Property(depends_on='task')

    #### TaskAction interface #################################################

    # The Task with which the action is associated. Set by the framework.
    task = Instance(Task)
    
    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_object(self):
        return self.task
    

class CentralPaneAction(TaskAction):
    """ An Action that makes a callback to a Task's central pane.
    """

    #### ListeningAction interface ############################################

    object = Property(depends_on='central_pane')

    #### CentralPaneAction interface ##########################################

    # The central pane with which the action is associated.
    central_pane = Property(Instance(TaskPane), depends_on='task')

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @cached_property
    def _get_central_pane(self):
        if self.task:
            return self.task.window.get_central_pane(self.task)
        return None

    def _get_object(self):
        return self.central_pane


class EditorAction(CentralPaneAction):
    """ An action that makes a callback to the active editor in an editor pane.
    """
    
    #### ListeningAction interface ############################################

    object = Property(depends_on='central_pane.active_editor')

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_object(self):
        if self.central_pane is not None:
            return self.central_pane.active_editor
        return None
