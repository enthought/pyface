# Enthought library imports.
from enthought.pyface.action.api import Action, ActionItem, Group
from enthought.traits.api import Any, Bool, List, Instance, Property, Unicode

# Local imports.
from enthought.pyface.tasks.task import Task
from enthought.pyface.tasks.task_window import TaskWindow


class TaskToggleAction(Action):
    """ An action for activating a task.
    """

    #### 'Action' interface ###################################################

    checked = Property(Bool, depends_on='task.window.active_task')
    name = Property(Unicode, depends_on='task.name')
    style = 'toggle'
    tooltip = Property(Unicode, depends_on='name')

    #### 'TaskActivateAction' interface #######################################
    
    task = Instance(Task)
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event=None):
        window = self.task.window
        window.activate_task(self.task)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_checked(self):
        window = self.task.window
        return window is not None and window.active_task == self.task

    def _get_name(self):
        return self.task.name

    def _get_tooltip(self):
        return u'Switch to the %s task.' % self.name


class TaskToggleGroup(Group):
    """ A menu for changing the active task in a task window.
    """

    #### 'ActionManager' interface ############################################

    id = 'TaskToggleGroup'
    items = List

    #### 'TaskChangeMenuManager' interface ####################################

    # The ActionManager to which the group belongs.
    manager = Any

    # The window that contains the group.
    window = Instance(TaskWindow)
        
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_items(self):
        items = []
        for task in self.window.tasks:
            action = TaskToggleAction(task=task)
            items.append(ActionItem(action=action))
        return items

    def _rebuild(self):
        # Clear out the old group, then build the new one.
        self.destroy()
        self.items = self._get_items()

        # Inform our manager that it needs to be rebuilt.
        self.manager.changed = True
        
    #### Trait initializers ###################################################

    def _items_default(self):
        self.window.on_trait_change(self._rebuild, 'tasks[]')
        return self._get_items()

    def _manager_default(self):
        manager = self
        while isinstance(manager, Group):
            manager = manager.parent
        return manager
    
    def _window_default(self):
        return self.manager.controller.task.window
