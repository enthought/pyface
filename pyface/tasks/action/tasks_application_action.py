# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
from traits.api import Instance

from pyface.action.api import GUIApplicationAction
from pyface.tasks.tasks_application import TasksApplication
from pyface.tasks.task_window_layout import TaskWindowLayout


class TasksApplicationAction(GUIApplicationAction):

    #: The Tasks application the action applies to.
    application = Instance(TasksApplication)


class CreateTaskWindowAction(TasksApplicationAction):
    """ A standard 'New Window' menu action. """

    name = "New Window"
    accelerator = "Ctrl+N"

    #: The task window wayout to use when creating the new window.
    layout = Instance("pyface.tasks.task_window_layout.TaskWindowLayout")

    def perform(self, event=None):
        window = self.application.create_window(layout=self.layout)
        self.application.add_window(window)

    def _layout_default(self):
        if self.application.default_layout:
            layout = self.application.default_layout[0]
        else:
            layout = TaskWindowLayout()
            if self.task_factories:
                layout.items = [self.task_factories[0].id]
        return layout
