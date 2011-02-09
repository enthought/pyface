# Enthought library imports.
from enthought.pyface.action.api import Action, Group, MenuManager
from enthought.traits.api import Bool, List, Instance, Property, Unicode, \
    on_trait_change

# Local imports.
from enthought.pyface.tasks.task import Task


class TaskChangeMenuManager(MenuManager):
    """ A menu for changing the active task in a task window.
    """

    #### 'ActionManager' interface ############################################

    id = 'TaskChangeMenu'
    name = 'Task'
    groups = List(Group)
    visible = Property(Bool, depends_on='window.tasks')

    #### 'TaskChangeMenuManager' interface ####################################

    window = Property(Instance('enthought.pyface.tasks.task_window.TaskWindow'),
                      depends_on='controller.task.window')

    ###########################################################################
    # 'TaskChangeMenuManager' interface.
    ###########################################################################

    def get_groups(self):
        """ Gets the groups for the menu based on the tasks currently attached
            to the window.
        """
        actions = []
        if self.window is not None:
            for task in self.window.tasks:
                actions.append(TaskActivateAction(task=task))
        return [ Group(*actions, id='TaskChangeGroup') ]

    @on_trait_change('window.tasks')
    def rebuild(self):
        """ Re-build the menu.
        """
        # Clear out the old menu. This gives any actions that have trait
        # listeners a chance to unhook them.
        self.destroy()
        
        self.groups = self.get_groups()
        
    ###########################################################################
    # Protected interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _groups_default(self):
        return self.get_groups()

    #### Trait property getter/setters ########################################

    def _get_visible(self):
        """ Only show the menu if the window has multiple tasks.
        """
        return self.window is not None and len(self.window.tasks) > 1

    def _get_window(self):
        """ Get the TaskWindow from our controller.
        """
        if self.controller is not None:
            return self.controller.task.window
        return None


class TaskActivateAction(Action):
    """ An action for activating a task.
    """

    #### 'TaskActivateAction' interface #######################################
    
    task = Instance(Task)
    
    #### 'Action' interface ###################################################

    name = Property(Unicode, depends_on='task.name')
    enabled = Property(Bool, depends_on='task.window.active_task')
    tooltip = Property(Unicode, depends_on='name')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event=None):
        window = self.task.window
        window.activate_task(self.task)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_name(self):
        return self.task.name

    def _get_enabled(self):
        window = self.task.window
        return window is not None and not window.active_task == self.task

    def _get_tooltip(self):
        return u'Switch to the %s task.' % self.name
