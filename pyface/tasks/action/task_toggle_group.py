# Copyright (c) 2010-18, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

# Enthought library imports.
from pyface.action.api import Action, ActionItem, Group
from traits.api import Any, List, Instance, Property, Unicode, on_trait_change

# Local imports.
from pyface.tasks.task import Task
from pyface.tasks.task_window import TaskWindow


class TaskToggleAction(Action):
    """ An action for activating a task.
    """

    #### 'Action' interface ###################################################

    #: The user-visible name of the action, matches the task name.
    name = Property(Unicode, depends_on='task.name')

    #: The action is a toggle menu item.
    style = 'toggle'

    #: The tooltip to display for the menu item.
    tooltip = Property(Unicode, depends_on='name')

    #### 'TaskActivateAction' interface #######################################

    task = Instance(Task)

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def destroy(self):
        super(TaskToggleAction, self).destroy()

        # Make sure that we are not listening to changes in the task anymore
        # In traits style, we will set the basic object to None and have the
        # listener check that if it is still there.
        self.task = None

    def perform(self, event=None):
        window = self.task.window
        window.activate_task(self.task)

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_name(self):
        if self.task is None:
            return 'UNDEFINED'
        return self.task.name

    def _get_tooltip(self):
        return u'Switch to the %s task.' % self.name

    @on_trait_change('task.window.active_task')
    def _update_checked(self):
        if self.task:
            window = self.task.window
            self.checked = (
                window is not None and window.active_task == self.task
            )


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
        if len(self.window.tasks) > 1:
            # at least two tasks, so something to toggle
            items = [
                ActionItem(
                    action=TaskToggleAction(task=task),
                ) for task in self.window.tasks
            ]
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