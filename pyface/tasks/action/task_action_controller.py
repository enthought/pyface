# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.action.api import ActionController
from traits.api import Instance


from pyface.tasks.task import Task
from pyface.tasks.action.task_action import TaskAction


class TaskActionController(ActionController):
    """ An action controller for menu and tool bars.

    The controller is used to 'hook' the invocation of every action on the menu
    and tool bars. This is done so that additional, Task-specific information
    can be added to action events. Currently, we attach a reference to the Task.
    """

    # TaskActionController interface ---------------------------------------

    #: The task that this is the controller for.
    task = Instance(Task)

    # ------------------------------------------------------------------------
    # 'ActionController' interface.
    # ------------------------------------------------------------------------

    def perform(self, action, event):
        """ Control an action invocation.
        """
        event.task = self.task
        return action.perform(event)

    def add_to_menu(self, item):
        """ Called when an action item is added to a menu/menubar.
        """
        action = item.item.action
        if isinstance(action, TaskAction):
            action.task = self.task

    def add_to_toolbar(self, item):
        """ Called when an action item is added to a toolbar.
        """
        action = item.item.action
        if isinstance(action, TaskAction):
            action.task = self.task
